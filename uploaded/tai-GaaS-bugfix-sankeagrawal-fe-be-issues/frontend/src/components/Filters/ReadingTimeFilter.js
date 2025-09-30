import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, FormGroup, FormControlLabel, Switch, Grid, Slider, Tooltip, Typography } from "@mui/material";
import { Context } from "../../Store";

export default function ReadingTimeFilter(props) {
    const {filterName, helperText} = props;
    const marks = [{value: 1, label: '1'}, {value: 20, label: '20'}];
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "ReadingTime_OUTPUT", enabled: event.target.checked});
    };

    const handleThreshold = (event, newValue) => {
        dispatch({type: "ReadingTime_OUTPUT", max_time: newValue})
    };

    const handleTruncate = (event) => {
        dispatch({type: "ReadingTime_OUTPUT", truncate: event.target.checked});
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.ReadingTime_OUTPUT.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Typography sx={{ mb: 5 }}>Max time (in minutes)</Typography>
                        <Slider
                            value={state.ReadingTime_OUTPUT.max_time}
                            onChange={handleThreshold}
                            valueLabelDisplay="on"
                            marks={marks}
                            step={1}
                            min={1}
                            max={20}/>
                        <FormGroup sx={{ mt: 5 }}>
                            <FormControlLabel control={<Switch checked={state.ReadingTime_OUTPUT.truncate} onChange={handleTruncate}/>} label="Truncate text to fit within the time limit?" />
                        </FormGroup>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}