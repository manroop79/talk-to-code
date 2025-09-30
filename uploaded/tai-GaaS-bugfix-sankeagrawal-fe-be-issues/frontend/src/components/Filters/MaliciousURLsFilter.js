import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Switch, Grid, Slider, Tooltip, Typography } from "@mui/material";
import { Context } from "../../Store";

export default function MaliciousURLsFilter(props) {
    const {filterName, helperText} = props;
    const marks = [{value: 0, label: '0'}, {value: 1, label: '1'}];
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "MaliciousURLs_OUTPUT", enabled: event.target.checked});
    };

    const handleThreshold = (event, newValue) => {
        dispatch({type: "MaliciousURLs_OUTPUT", threshold: newValue})
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.MaliciousURLs_OUTPUT.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Typography sx={{ mb: 5 }}>Threshold</Typography>
                        <Slider
                            value={state.MaliciousURLs_OUTPUT.threshold}
                            onChange={handleThreshold}
                            valueLabelDisplay="on"
                            marks={marks}
                            step={0.05}
                            min={0}
                            max={1}/>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}