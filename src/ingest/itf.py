"""Parser for the MPC Isolated Tracklet File (for the 80-column astrometry format).""" #the file's docstring (self description)
import pandas as pd #pandas, used to build the dataframe

def parse_line(line): #starts a function definition, takes one input, line
    """Takes one raw line of text. Then returns a dictionar (dict) of its fields, or  none if the line has been determine that it should be skipped.""" #this function's docstring
    if len(line) < 80:
        return None #ends the function, hands the value back (just skips the line)
    if line[14].islower():
        return None #if the line is flagged, we skip it, as it would mess with the rest of the parser
    off = 0 if line[15].isdigit() else 1 #detects if there's a line shift
    return{
        "desig":    line[:12].strip(), #defines the designation field on our new table as characters 0 through 11. .strip() removes the spaces including in the line for "padding"
        "date_str": line[15+off:32+off].strip(), #This line and the following three all do the same, but for other values
        "ra_str":   line[32+off:44+off].strip(),
        "dec_str":  line[44+off:56+off].strip(),
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