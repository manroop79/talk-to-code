import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Checkbox, FormControl, FormLabel, FormGroup, FormControlLabel, Switch, Grid, Tooltip, TextField } from "@mui/material";
import { Context } from "../../Store";

export default function CodeFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const LANGUAGES = ["go", "java", "javascript", "php", "python", "ruby"];
    const [state, dispatch] = useContext(Context);

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.Code.enabled : state.Code_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "CODE" : "CODE_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={LANGUAGES}
                            value={CurrentPage === "input" ? state.Code.languages : state.Code_OUTPUT.languages}
                            multiple
                            onChange={(e, value, situation, option) => dispatch({type: CurrentPage === "input" ? "CODE" : "CODE_OUTPUT", languages: typeof value === 'string' ? value.split(",") : value})}
                            renderInput={(params) => ( <TextField {...params} label="Programming Languages..." /> )}
                        />
                        <FormControl sx={{ mt: 5 }}>
                            <Grid container item direction="row" justifyContent="space-between" alignItems="center">
                                <FormLabel>Options</FormLabel>
                                <Tooltip title="This determines how the languages are treated. If checked, any selected language present in the prompt marks the prompt as invalid; if unchecked, the prompt is considered valid if it contains any selected language." placement="right">
                                    <HelpOutlineIcon/>
                                </Tooltip>
                                </Grid>
                                    <FormGroup>
                                        <FormControlLabel control={<Checkbox checked={CurrentPage === "input" ? state.Code.is_blocked : state.Code_OUTPUT.is_blocked} onChange={(event) => dispatch({type: CurrentPage === "input" ? "CODE" : "CODE_OUTPUT", is_blocked: event.target.checked})}/>} label="Blocked" />
                                    </FormGroup>
                        </FormControl>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}