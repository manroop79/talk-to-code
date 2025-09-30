import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Switch, Checkbox, Chip, Divider, FormControl, FormControlLabel, FormGroup, FormLabel, Grid, Radio, RadioGroup, TextField, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function PromptInjectionFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.Regex.enabled : state.Regex_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "REGEX" : "REGEX_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={[]}
                            value={CurrentPage === "input" ? state.Regex.patterns : state.Regex_OUTPUT.patterns}
                            freeSolo
                            multiple
                            onChange={(e, value, situation, option) => dispatch({type: CurrentPage === "input" ? "REGEX" : "REGEX_OUTPUT", patterns: typeof value === 'string' ? value.split(",") : value})}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => ( <Chip label={option} {...getTagProps({ index })} /> ))
                            }
                            renderInput={(params) => (
                                <TextField {...params}
                                    sx={{ mb: 3 }}
                                    label="Type patterns here (press Enter after each)"
                                    multiline
                                    fullWidth/>)}
                        />
                        <Grid container direction="row" justifyContent="space-around" alignItems="center">
                            <FormControl>
                                <FormLabel>Match Type</FormLabel>
                                <RadioGroup
                                    value={CurrentPage === "input" ? state.Regex.match_type : state.Regex_OUTPUT.match_type}
                                    onChange={(event) => dispatch({type: CurrentPage === "input" ? "REGEX" : "REGEX_OUTPUT", match_type: event.target.value})}>
                                    <FormControlLabel value="search" control={<Radio />} label="Search" />
                                    <FormControlLabel value="full_match" control={<Radio />} label="Full Match" />
                                </RadioGroup>
                            </FormControl>
                            <Divider orientation="vertical" flexItem/>
                            <FormControl>
                                <FormLabel>Options</FormLabel>
                                    <Grid container item direction="row" justifyContent="space-between" alignItems="center">
                                        <FormGroup>
                                            <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.Regex.is_blocked : state.Regex_OUTPUT.is_blocked} onChange={(event) => dispatch({type: CurrentPage === "input" ? "REGEX" : "REGEX_OUTPUT", is_blocked: event.target.checked})}/>} label="Blocked" />
                                        </FormGroup>
                                        <Tooltip title="This determines how the patterns are treated. If checked, any pattern match marks the prompt as invalid; if unchecked, the prompt is considered valid if it matches any of the patterns." placement="right">
                                            <HelpOutlineIcon/>
                                        </Tooltip>
                                    </Grid>
                                    <Grid container item direction="row" justifyContent="space-between" alignItems="center">
                                        <FormGroup>
                                            <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.Regex.redact : state.Regex_OUTPUT.redact} onChange={(event) => dispatch({type: CurrentPage === "input" ? "REGEX" : "REGEX_OUTPUT", redact: event.target.checked})}/>} label="Redact" />
                                        </FormGroup>
                                        <Tooltip title="Replace the matched patterns with [REDACTED]" placement="right">
                                            <HelpOutlineIcon/>
                                        </Tooltip>
                                    </Grid>
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