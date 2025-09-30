import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Chip, Switch, Checkbox, Divider, FormControl, FormControlLabel, FormGroup, FormLabel, Grid, Radio, RadioGroup, TextField, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function BanSubstringsFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.BanSubstrings.enabled : state.BanSubstrings_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={[]}
                            value={CurrentPage === "input" ? state.BanSubstrings.substrings : state.BanSubstrings_OUTPUT.substrings}
                            freeSolo
                            multiple
                            onChange={(e, value, situation, option) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", substrings: typeof value === 'string' ? value.split(",") : value})}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => ( <Chip label={option} {...getTagProps({ index })} /> ))
                            }
                            renderInput={(params) => (
                                <TextField {...params}
                                    sx={{ mb: 3 }}
                                    label="Type strings here (press Enter after each)"
                                    multiline
                                    fullWidth/>)}
                        />
                        <Grid container direction="row" justifyContent="space-around" alignItems="center">
                            <FormControl>
                                <FormLabel>Match Type</FormLabel>
                                <RadioGroup
                                    value={CurrentPage === "input" ? state.BanSubstrings.match_type : state.BanSubstrings_OUTPUT.match_type}
                                    onChange={(event) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", match_type: event.target.value})}>
                                    <FormControlLabel value="str" control={<Radio />} label="String" />
                                    <FormControlLabel value="word" control={<Radio />} label="Word" />
                                </RadioGroup>
                            </FormControl>
                            <Divider orientation="vertical" flexItem/>
                            <FormControl>
                            <FormLabel>Options</FormLabel>
                            <FormGroup>
                                <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.BanSubstrings.case_sensitive : state.BanSubstrings_OUTPUT.case_sensitive} onChange={(event) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", case_sensitive: event.target.checked})} />} label="Case Sensitive" />
                                <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.BanSubstrings.redact : state.BanSubstrings_OUTPUT.redact} onChange={(event) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", redact: event.target.checked})}/>} label="Redact" />
                                <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.BanSubstrings.contains_all : state.BanSubstrings_OUTPUT.contains_all} onChange={(event) => dispatch({type: CurrentPage === "input" ? "SUBSTRINGS" : "SUBSTRINGS_OUTPUT", contains_all: event.target.checked})}/>} label="Contains All" />
                            </FormGroup>
                        </FormControl>
                        </Grid>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}