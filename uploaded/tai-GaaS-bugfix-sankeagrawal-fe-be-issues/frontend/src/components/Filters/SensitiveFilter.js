import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Checkbox, FormControl, FormControlLabel, FormGroup, FormLabel, Link, Switch, TextField, Grid, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function SensitiveFilter(props) {
    const {filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);
    const EntityOptions = ["CREDIT_CARD", "CRYPTO", "DATE_TIME", "EMAIL_ADDRESS", "IBAN_CODE", "IP_ADDRESS", "NRP", "LOCATION", "PERSON", "PHONE_NUMBER", "MEDICAL_LICENSE", "URL", "US_BANK_NUMBER", "US_DRIVER_LICENSE", "US_ITIN", "US_PASSPORT", "US_SSN"];

    const handleCheck = (event) => {
        dispatch({type: "Sensitive_OUTPUT", enabled: event.target.checked});
    };

    const handleEntity_Chip = (e, value, situation, option) => {
        dispatch({type: "Sensitive_OUTPUT", entity_types: typeof value === 'string' ? value.split(",") : value});
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.Sensitive_OUTPUT.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={EntityOptions}
                            value={state.Sensitive_OUTPUT.entity_types}
                            multiple
                            onChange={handleEntity_Chip}
                            renderInput={(params) => ( <TextField {...params} label="Sensitive Entities..." helperText={<Link target="_blank" href="https://microsoft.github.io/presidio/supported_entities/#list-of-supported-entities">List of supported entities</Link>} /> )}
                        />
                        <FormControl sx={{ mt: 5 }}>
                            <Grid container item direction="row" justifyContent="space-between" alignItems="center">
                                <FormLabel>Options</FormLabel>
                                <Tooltip title="When checked, the redact feature ensures sensitive entities are seamlessly replaced." placement="right">
                                    <HelpOutlineIcon/>
                                </Tooltip>
                                </Grid>
                                    <FormGroup>
                                        <FormControlLabel control={<Checkbox checked={state.Sensitive_OUTPUT.redact} onChange={(event) => dispatch({type: "Sensitive_OUTPUT", redact: event.target.checked})}/>} label="Redact" />
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