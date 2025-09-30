import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Chip, FormGroup, FormControlLabel, Link, Switch, TextField, Grid, Slider, Tooltip, Typography } from "@mui/material";
import { Context } from "../../Store";

export default function AnonymizeFilter(props) {
    const {filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);
    const marks = [{value: 0, label: '0'}, {value: 1, label: '1'}];
    const EntityOptions = ["CREDIT_CARD", "CRYPTO", "DATE_TIME", "EMAIL_ADDRESS", "IBAN_CODE", "IP_ADDRESS", "NRP", "LOCATION", "PERSON", "PHONE_NUMBER", "MEDICAL_LICENSE", "URL", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN"];

    const handleCheck = (event) => {
        dispatch({type: "ANONYMIZE", enabled: event.target.checked});
    };

    const handleEntity_Chip = (e, value, situation, option) => {
        dispatch({type: "ANONYMIZE", entity_types: typeof value === 'string' ? value.split(",") : value});
    };

    const handleHiddenName_Chip = (e, value, situation, option) => {
        dispatch({type: "ANONYMIZE", hidden_names: typeof value === 'string' ? value.split(",") : value});
    }
    
    const handleAllowedName_Chip = (e, value, situation, option) => {
        dispatch({type: "ANONYMIZE", allowed_names: typeof value === 'string' ? value.split(",") : value});
    }

    const handleFakerCheck = (event) => {
        dispatch({type: "ANONYMIZE", use_faker: event.target.checked});
    };

    const handleThreshold = (event, newValue) => {
        dispatch({type: "ANONYMIZE", threshold: newValue})
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.Anonymize.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={EntityOptions}
                            value={state.Anonymize.entity_types}
                            multiple
                            onChange={handleEntity_Chip}
                            renderInput={(params) => ( <TextField {...params} label="Entities to anonymize..." helperText={<Link target="_blank" href="https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities">List of supported entities</Link>} /> )}
                        />
                        <Autocomplete
                            clearIcon={false}
                            options={[]}
                            value={state.Anonymize.hidden_names}
                            freeSolo
                            multiple
                            onChange={handleHiddenName_Chip}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => ( <Chip label={option} {...getTagProps({ index })} /> ))
                            }
                            renderInput={(params) => ( <TextField {...params} sx={{ mt: 5 }} label="Names to be hidden/anonymized..." helperText="These names will be hidden e.g. [REDACTED_CUSTOM1]." multiline fullWidth/> )}
                        />
                        <Autocomplete
                            clearIcon={false}
                            options={[]}
                            value={state.Anonymize.allowed_names}
                            freeSolo
                            multiple
                            onChange={handleAllowedName_Chip}
                            renderTags={(value, getTagProps) =>
                                value.map((option, index) => ( <Chip label={option} {...getTagProps({ index })} /> ))
                            }
                            renderInput={(params) => ( <TextField {...params} sx={{ mt: 5 }} label="Names to be ignored..." helperText="These names will not be redacted even if flagged by the detector." multiline fullWidth/> )}
                        />
                        <TextField sx={{ mt: 5 }} label="Preamble" helperText="Directs the LLM to bypass/skip specific content" multiline fullWidth value={state.Anonymize.preamble} onChange={(e) => {dispatch({type: "ANONYMIZE", preamble: e.target.value})}}/>
                        <FormGroup sx={{ mt: 5 }}>
                            <FormControlLabel control={<Switch checked={state.Anonymize.use_faker} onChange={handleFakerCheck}/>} label="Use Faker library to generate fake data?" />
                        </FormGroup>
                        <Typography sx={{ mt: 5 }}>Threshold</Typography>
                        <Slider
                            value={state.Anonymize.threshold}
                            onChange={handleThreshold}
                            valueLabelDisplay="on"
                            marks={marks}
                            step={0.10}
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