"""Parser for the MPC Isolated Tracklet File (for the 80-column astrometry format).""" #the file's docstring (self description)
import pandas as pd #pandas, used to build the dataframe
from collections import Counter #tally-dict, essentially removes init sequence
import re #allows me to only build the validator pattern once
from astropy.coordinates import SkyCoord #used to help convert ra_deg and dec_deg to degrees.
import astropy.units as u #also helped for the conversion of units
from datetime import datetime, timedelta #used to help convert the timestamp
import os #used to create an output folder

def _ra_hours_ok(ra): #checks if the hours field is believable
    parts = ra.split()
    return bool(parts) and parts[0].isdigit() and int(parts[0]) < 24

def parse_line(line): #starts a function definition, takes one input, line
    """Takes one raw line of text. Then returns a dictionar (dict) of its fields, or  none if the line has been determine that it should be skipped.""" #this function's docstring
    if len(line) < 80:
        return None #ends the function, hands the value back (just skips the line)
    if line[14].islower():
        return None #if the line is flagged, we skip it, as it would mess with the rest of the parser
    off = 0 if line[15].isdigit() else 1 #detects if there's a line shift

    ra_str = line[32+off:44+off].strip() #where the RA normally lives
    fmt = "standard"
    if not _ra_hours_ok(ra_str): #if there are impossible hours, it will try the layout with the long date.
        ra_str = line[35+off:43+off].strip()
        fmt = "long_date"
        if not _ra_hours_ok(ra_str): #still impossible means unreadable.
            return None
    dec_str = line[44+off:56+off].strip()
    if coord_issues(ra_str, dec_str):
        return None

    return{
        "desig":    line[:12].strip(), #defines the designation field on our new table as characters 0 through 11. .strip() removes the spaces including in the line for "padding"
        "date_str": line[15+off:32+off].strip(), #This line and the following three all do the same, but for other values
        "ra_str":   ra_str,
        "dec_str":  dec_str,
        "fmt":      fmt,
        "obscode":  line[77+off:80+off], #observatory code, for the last three columns

    } #end of return

def parse_itf(path, max_lines=None): #creates my second function, takes in a file path, and an optional input, defaulting the max lines to None if not provided by the caller
    """Takes a file path. Returns (dataframe, stats dict)."""
    rows = []
    stats = {"parsed": 0, "skipped": 0} #this and above make up the accumilator list
    with open(path) as f: #opens the file provided by the caller. "with" ensures the file gets closed when the block ends, even if something crashes
        for i, line in enumerate(f): #loops directly over the file handle, which is really efficent, because it only loads one line at a time, but it doesn't load the entire file into memory, allowing this function to scale to the level of the ITF. 
            if max_lines is not None and i >= max_lines: 
                break #this if checks if we've hit the limit provided by the caller, and abandons the loop entirely if so
            rec = parse_line(line.rstrip("\n")) #this is the "handoff" between two functions. lines from a file arrive with an invisiable character at the end, .rstrip(\n) trims that off, so as not to break the parser logic
            if rec is None:
                stats["skipped"] += 1
            else:
                rows.append(rec)
                stats["parsed"] += 1 #another part of the seperation
    return pd.DataFrame(rows), stats #builds the table from the accumilated dicts of all the lines, and returns two things at once. 

def census_itf(path):
    """Only goes through the file once, kept only the counters instead of the data itself."""
    obs = Counter() #obscode = how many observations
    years = Counter() #year = how many observations
    sizes = Counter() #desig = how many observations
    ra_ok = re.compile(r"^\d{2} \d{2} \d{2}") #pre-built validator
    stats = {"parsed": 0, "skipped": 0, "bad_ra": 0}
    with open(path) as f:
        for line in f:
            rec = parse_line(line.rstrip("/n")) #parses the line, after stripping it of spaces and removing invisible end character
            if rec is None:
                stats["skipped"] += 1
                continue
            stats["parsed"] += 1
            obs[rec["obscode"]] += 1
            years[rec["date_str"][:4]] += 1
            sizes[rec["desig"]] += 1
            if not ra_ok.match(rec["ra_str"]): #tests one string
                stats["bad_ra"] += 1
    return obs, years, sizes, stats

def _parse_date(s): #just as used before, will convert the time to real usable timestamps
    """'2015 05 23.30928' to real timestamp."""
    y, m, d = s.split()
    day_frac = float(d)
    day = int(day_frac)
    return datetime(int(y), int(m), day) + timedelta(days=day_frac - day)

def to_numeric(df): #converts ra_deg and dec_deg into real degrees, also applies _parse_date to the time column
    """Adds ra_deg, dec_deg, time columns to a fully parsed ITF table. returns df."""
    coords = SkyCoord(df["ra_str"], df["dec_str"], unit=(u.hourangle, u.deg))
    df["ra_deg"] = coords.ra.deg
    df["dec_deg"]  = coords.dec.deg
    df["time"] = df["date_str"].apply(_parse_date)
    return df

def parse_itf_numeric(path, batch_size=500000, keep=None): #path has the caller tell us which file to read. both batch size and keep have defaults, so they're not required. 
    """This function will impliment batch parsing, or chunk parsing, by parsing the entire ITF in batches, converting to numbers, and returning one table."""
    #the below is for variable creation
    batch = [] #an empty list for holding the parsed rows
    done = [] #an empty list for the compacted table
    total = 0 #counter starting at zero
    with open(path) as f: #open(path) opens the file for reading, as f names it f, it also automatically closes the file when the block end, even with an error partway.
        for line in f: #looping through the entire file will give me one mile at a time, so not all of the massive file ever enters all of the memory at once. line is a string.
            row = parse_line(line) #calls my own parser, outputs a dictionary of fields
            if row: #acts as a "truth test." if the dictionary is not filled, this will skip over it
                batch.append(row) #adds the successful dictionaries onto the end of the batch list.
            if len(batch) >= batch_size: #once the number of rows collected reaches the batch size, it will compact them and then dump them from the memory.  >= for safety, so an overshoot would sitll trigger.
                piece = to_numeric(pd.DataFrame(batch)) #converts dec_deg, ra_deg and time columns in the freshly made table into usable numbers.
                done.append(piece[keep] if keep else piece) #if the caller named columns, store only those columns, otherwise store everything. then, .append(...) files the now finished piece into done.
                total += len(batch) #adds the length of the now completed batch to total, to calculate the end quantity of lines parsed. Must happen before next line, because the next next line because then batch will be emptied.
                print(f"{total:,} rows done") #a "heartbeat." will update at the end of the completion with number of rows parsed. also formats the numbers with commas.
                batch = [] #fully clears batch, freeing a bunch of memory. Batch was already added to done, which takes up much less space, as it doesn't have strings, so there are only ever batch number of rows with strings in them, massivly reducing the memory costs.
        if batch: #runs once, after every line has been read. this is because the number of rows int the ITF will not break evenly into 500,000s, so this will check for any remaining rows
            #same three lines as before. No need to clear batch though.
            piece = to_numeric(pd.DataFrame(batch))
            done.append(piece[keep] if keep else piece)
            total += len(batch)

    return pd.concat(done, ignore_index=True) #stacks all the small tables in done into one large table, as we want. ignore_index=Truewill renumber the entire file cleanly.

def coord_issues(ra, dec): #this function takes in two inputs, the RA string and the Dec string. will return a list of problem labels
    bad = [] #an empty list to collect the names of any problems found
    rp = ra.split() #splits the RA styring into peices.
    try: #starts a try block, will jump to except if something breaks.
        if len(rp) not in (2, 3): bad.append("ra_fields") #a valid RA has two peices. Any other count is wrong
        if not (0 <= abs(float(rp[0])) < 24): bad.append("ra_hr") #the first piece of an RA field is hours. This will convert it to a number, drop any sign with abs, and require 0-24
        if len(rp) >= 2 and not (0 <= float(rp[1]) < 60): bad.append("ra_min") #if there is a second piece (minutes), then it will require 0-60. Out of range will return ra_min
        if len(rp) == 3 and not (0 <= float(rp[2]) < 60): bad.append("ra_sec") #if there is a third piece (seconds), then it will require 0-60, or return ra_sec
    except (ValueError, IndexError): bad.append("ra_parse") #if any of the above RA checks threw a ValueError, or was missing a peice, it will return "ra_parse", meaning it simply couldn't read the RA at all
    dp = dec.split() #uses the same idea as for RA, but for Dec, splits into pieces. dp = all the dec parts
    try:
        if len(dp) != 3: bad.append("dec_fields") #the dec data is ALWAYS in 3 peices, and there is no short form like RA, so anything other than 3 is simply wrong.
        #the below two ifs are for the minutes and seconds range checks
        if len(dp) >= 2 and not (0 <= float(dp[1]) < 60): bad.append("dec_min")
        if len(dp) == 3 and not (0 <= float(dp[2]) < 60): bad.append("dec_sec")
    except (ValueError, IndexError): bad.append("dec_parse") #the "catch-all" for an unredable Dec value
    return bad #hands back the "list of problems."

def parse_itf_to_parts(path, out_dir, batch_size=500_000, keep=None):
    """Parse the ITF in batches, writing each batch to its own file, so the memory never fills."""
    os.makedirs(out_dir, exist_ok=True) #creates the output folder. exist_ok=True means dont cause an error if it already exists, making re-running this file to fix errors safe
    total, part, batch = 0, 0, [] #creates three counters in one line, one for the rows written so far, one for which part-file number we're on, and one for the current batch
    with open(path) as f:
        for line in f:
            row = parse_line(line)
            if row: #if it's a real row, adds it to the batch
                batch.append(row)
            if len(batch) >= batch_size:
                df = to_numeric(pd.DataFrame(batch)) #turns the batch into a table, and adds the numeric tables.
                if keep: #narrows to only the columns that I want
                    df = df[keep]
                df.to_parquet(f"{out_dir}/part_{part:03d}.parquet") #writes this batch to its own file, pads the number to 3 digits so files sort correctly.
                total += len(df) #adds batch size to total
                part += 1
                print(f"{total:,} rows written") #the "heartbeat," prints out the total after every batch
                batch = [] #clears batch
        if batch: #this block parses the batch made up of the leftover frames.
            df = to_numeric(pd.DataFrame(batch))
            if keep:
                df = df[keep]
            df.to_parquet(f"{out_dir}/part_{part:03d}.parquet")
        return total