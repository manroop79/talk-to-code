import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Switch, Chip, Grid, Slider, Typography, TextField, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function BanTopicsFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const marks = [{value: 0, label: '0'}, {value: 1, label: '1'}];
    const [state, dispatch] = useContext(Context);

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.BanTopics.enabled : state.BanTopics_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "TOPICS" : "TOPICS_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={[]}
                            value={CurrentPage === "input" ? state.BanTopics.topics : state.BanTopics_OUTPUT.topics}
                            freeSolo
                            multiple
                            onChange={(e, value, situation, option) => dispatch({type: CurrentPage === "input" ? "TOPICS" : "TOPICS_OUTPUT", topics: typeof value === 'string' ? value.split(",") : value})}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => ( <Chip label={option} {...getTagProps({ index })} /> ))
                            }
                            renderInput={(params) => (
                                <TextField {...params}
                                    sx={{ mb: 3 }}
                                    label="Type topics here (press Enter after each)"
                                    multiline
                                    fullWidth/>)}
                        />
                        <Typography sx={{ mb: 5 }}>Threshold</Typography>
                        <Slider
                            value={CurrentPage === "input" ? state.BanTopics.threshold : state.BanTopics_OUTPUT.threshold}
                            onChange={(event, newValue) => dispatch({type: CurrentPage === "input" ? "TOPICS" : "TOPICS_OUTPUT", threshold: newValue})}
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