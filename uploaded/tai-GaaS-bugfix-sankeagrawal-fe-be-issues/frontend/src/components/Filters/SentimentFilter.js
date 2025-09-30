import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Switch, Grid, Slider, Tooltip, Typography } from "@mui/material";
import { Context } from "../../Store";

export default function SentimentFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const marks = [{value: -1, label: '-1'}, {value: 0, label: '0'}, {value: 1, label: '1'}];
    const [state, dispatch] = useContext(Context);

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.Sentiment.enabled : state.Sentiment_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "SENTIMENT" : "SENTIMENT_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Grid container direction="row" justifyContent="flex-start" alignItems="flex-start">
                            <Typography sx={{ mb: 5 }}>Threshold</Typography>
                            <Tooltip title="Negative values are negative sentiment, positive values are positive sentiment" placement="right">
                                <HelpOutlineIcon/>
                            </Tooltip>
                        </Grid>
                        <Slider
                            value={CurrentPage === "input" ? state.Sentiment.threshold : state.Sentiment_OUTPUT.threshold}
                            onChange={(event, newValue) => dispatch({type: CurrentPage === "input" ? "SENTIMENT" : "SENTIMENT_OUTPUT", threshold: newValue})}
                            valueLabelDisplay="on"
                            marks={marks}
                            step={0.1}
                            min={-1}
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