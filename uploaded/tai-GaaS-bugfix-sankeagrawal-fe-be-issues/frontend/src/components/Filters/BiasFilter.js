import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, FormControl, FormControlLabel, FormLabel, Radio, Switch, Grid, RadioGroup, Slider, Tooltip, Typography } from "@mui/material";
import { Context } from "../../Store";

export default function BiasFilter(props) {
    const {filterName, helperText} = props;
    const marks = [{value: 0, label: '0'}, {value: 1, label: '1'}];
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "BIAS_OUTPUT", enabled: event.target.checked});
    };

    const handleThreshold = (event, newValue) => {
        dispatch({type: "BIAS_OUTPUT", threshold: newValue})
    };

    const handleMatchType = (event) => {
        dispatch({type: "BIAS_OUTPUT", match_type: event.target.value})
    }

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.Bias_OUTPUT.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Typography sx={{ mb: 5 }}>Threshold</Typography>
                        <Slider
                            value={state.Bias_OUTPUT.threshold}
                            onChange={handleThreshold}
                            valueLabelDisplay="on"
                            marks={marks}
                            step={0.05}
                            min={0}
                            max={1}/>
                        <FormControl sx={{ mt: 5 }}>
                            <Grid container item direction="row" justifyContent="space-between" alignItems="center">
                                <FormLabel>Match Type</FormLabel>
                                <Tooltip title="In sentence mode, the scanner scans each sentence to check for bias. In full mode, the entire text is scanned." placement="right">
                                    <HelpOutlineIcon/>
                                </Tooltip>
                                </Grid>
                                    <RadioGroup value={state.Bias_OUTPUT.match_type} onChange={handleMatchType}>
                                        <FormControlLabel value="sentence" control={<Radio />} label="Sentence" />
                                        <FormControlLabel value="full" control={<Radio />} label="Full" />
                                    </RadioGroup>
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