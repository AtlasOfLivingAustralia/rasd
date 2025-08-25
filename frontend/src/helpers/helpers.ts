// @ts-ignore
import isEmail from 'validator/es/lib/isEmail';
import isEmpty from 'validator/es/lib/isEmpty';
import isStrongPassword from 'validator/es/lib/isStrongPassword';
import isURL from 'validator/es/lib/isURL';
import isInt from 'validator/es/lib/isInt';
import { useProgrammatic } from '@oruga-ui/oruga-next';

export const abnRegex = new RegExp('^[1-9]{1}\\d{1}\\s?\\d{3}\\s?\\d{3}\\s?\\d{3}$');
/* eslint-disable */
const doiRegex = /\b10\.(\d+\.*)+[\ /]/;
const successClasses = 'is-success';
const warningClasses = 'is-warning';
const dangerClasses = 'is-danger';

type XorHasValueValidatorOptions = { xorField: string; xorValue: string | undefined; xnor: boolean };
type BothHaveValueValidatorOptions = {
  andField: string;
  andValue: string | undefined;
  xnor: boolean;
};
type ValidatorFunction<T, U> = (value: T, options?: U) => string | undefined;

// Generic validators
export const hasValueValidator: ValidatorFunction<string | boolean | undefined, undefined> = function (value) {
  const validBoolean = typeof value === 'boolean';
  const validString = typeof value === 'string' && !!value;
  // Return an error if the value is not a valid string or boolean, or if the field hasn't been touched yet
  return validBoolean || validString ? undefined : 'A value must be provided.';
};

export const xorHasValueValidator: ValidatorFunction<string | undefined, XorHasValueValidatorOptions> = function (
  value,
  options
) {
  const { xorField, xorValue } = options || {};
  // Don't return validation error messages if the field hasn't been touched
  let message: string | undefined;
  const noValue = !!hasValueValidator(value);
  const noXorValue = !!hasValueValidator(xorValue);
  if (noValue && noXorValue) {
    message = `This field must be filled if ${xorField} is empty`;
  } else if (!noValue && !noXorValue) {
    message = `This field must be blank if ${xorField} is filled`;
  }
  return message;
};

export const bothHaveValueValidator: ValidatorFunction<string | undefined, U> = function (
  value,
  options: BothHaveValueValidatorOptions
) {
  const { andField, andValue } = options;
  const firstHasValue = !hasValueValidator(value);
  const secondHasValue = !hasValueValidator(andValue);
  let message: string | undefined;
  // Also accept neither having a value
  if (!((firstHasValue && secondHasValue) || (options.xnor && !firstHasValue && !secondHasValue))) {
    if (!firstHasValue) {
      message = `This field must not be blank if '${andField}' has a value`;
    } else {
      message = `'${andField}' must not be blank if this field has a value`;
    }
  }
  return message;
};

export const emailValidator = (email: string): object => {
  const emailValid = isEmail(email);
  if (emailValid) {
    return { valid: emailValid, emailClasses: successClasses };
  }
  return { valid: emailValid, emailClasses: dangerClasses };
};

export const nameValidator = (name: string): object => {
  const nameValid = !isEmpty(name, { ignore_whitespace: true });
  if (nameValid) {
    return { valid: nameValid, nameClasses: successClasses };
  }
  return { valid: nameValid, nameClasses: dangerClasses };
};

export const passwordValidator = (password: string): object => {
  const passwordValid = isStrongPassword(password);
  if (passwordValid) {
    return { valid: passwordValid, passwordClasses: successClasses };
  }
  return { valid: passwordValid, passwordClasses: dangerClasses };
};

export const matchValidator = (field1: string, field2: string): object => {
  return field1 === field2
    ? { valid: true, matchClasses: successClasses }
    : { valid: false, matchClasses: dangerClasses };
};

export const abnValidator = (abn: string): object => {
  const abnValid = abn.match(abnRegex);
  if (abnValid) {
    return { valid: abnValid, abnClasses: successClasses };
  }
  return { valid: abnValid, abnClasses: dangerClasses };
};

export const titleValidator = (title: string): object => {
  //check if title is just empty whitespace
  const titleValid = !isEmpty(title, { ignore_whitespace: true });
  if (titleValid) {
    return { valid: titleValid, titleClasses: successClasses };
  }
  return { valid: titleValid, titleClasses: dangerClasses };
};

export const keywordsValidator = (keywords: []): object => {
  if (keywords === null || keywords.length === 0) {
    return {
      keywordClasses: dangerClasses,
      valid: false,
    };
  } else {
    return {
      keywordClasses: successClasses,
      valid: true,
    };
  }
};

export const temporalCoverageFromValidator = (temporalCoverageFrom: string): object => {
  if (temporalCoverageFrom) {
    return { valid: true, temporalCoverageFromClasses: successClasses };
  }
  return { valid: false, temporalCoverageFromClasses: dangerClasses };
};

export const temporalCoverageToValidator = (temporalCoverageTo: string): object => {
  if (temporalCoverageTo) {
    return { valid: true, temporalCoverageToClasses: successClasses };
  }
  return { valid: false, temporalCoverageToClasses: dangerClasses };
};

export const northCoordinateValidator = (coordinate: string): object => {
  if (coordinate !== null) {
    // @ts-ignore
    if (isInt(coordinate, { min: -90, max: 90 })) {
      return { valid: true, northBoundingCoordinateClasses: successClasses };
    }
  }
  return { valid: false, northBoundingCoordinateClasses: dangerClasses };
};

export const southCoordinateValidator = (coordinate: string): object => {
  if (coordinate !== null) {
    if (isInt(coordinate, { min: -90, max: 90 })) {
      return { valid: true, southBoundingCoordinateClasses: successClasses };
    }
  }
  return { valid: false, southBoundingCoordinateClasses: dangerClasses };
};

export const eastCoordinateValidator = (coordinate: string): object => {
  if (coordinate !== null) {
    if (isInt(coordinate, { min: -180, max: 180 })) {
      return { valid: true, eastBoundingCoordinateClasses: successClasses };
    }
  }
  return { valid: false, eastBoundingCoordinateClasses: dangerClasses };
};

export const westCoordinateValidator = (coordinate: string): object => {
  if (coordinate !== null) {
    if (isInt(coordinate, { min: -180, max: 180 })) {
      return { valid: true, westBoundingCoordinateClasses: successClasses };
    }
  }
  return { valid: false, westBoundingCoordinateClasses: dangerClasses };
};

export const locationsValidator = (locations: []): object => {
  if (locations === null || locations.length === 0) {
    return {
      locationsClasses: dangerClasses,
      valid: false,
    };
  } else {
    return {
      locationsClasses: successClasses,
      valid: true,
    };
  }
};

export const taxaValidator = (taxa: string): object => {
  if (!isEmpty(taxa, { ignore_whitespace: true })) {
    return { valid: true, taxaCoveredClasses: successClasses };
  }
  return { valid: false, taxaCoveredClasses: dangerClasses };
};

export const collectionValidator = (collection: []): object => {
  if (collection === null || collection.length === 0) {
    return { valid: false, collectionMethodsClasses: dangerClasses };
  }
  return { valid: true, collectionMethodsClasses: successClasses };
};

export const dataSourceValidator = (dataSourceDOI: string, dataSourceURL: string): object => {
  const dataSourceDOIValid = dataSourceDOI.match(doiRegex);
  const dataSourceURLValid = isURL(dataSourceURL, {
    protocols: ['http', 'https', 'ftp'],
    require_tld: true,
    require_protocol: true,
  });

  if (dataSourceDOIValid && dataSourceURL === '') {
    return { valid: true, dataSourceDOIClasses: successClasses, dataSourceURLClasses: warningClasses };
  }
  if (dataSourceDOI === '' && dataSourceURLValid) {
    return { valid: true, dataSourceDOIClasses: warningClasses, dataSourceURLClasses: successClasses };
  }
  if (dataSourceDOIValid && dataSourceURLValid) {
    return { valid: true, dataSourceDOIClasses: successClasses, dataSourceURLClasses: successClasses };
  }
  if (dataSourceDOIValid && !dataSourceURLValid) {
    return { valid: false, dataSourceDOIClasses: successClasses, dataSourceURLClasses: dangerClasses };
  }
  if (!dataSourceDOIValid && dataSourceURLValid) {
    return { valid: false, dataSourceDOIClasses: dangerClasses, dataSourceURLClasses: successClasses };
  }
  return { valid: false, dataSourceDOIClasses: dangerClasses, dataSourceURLClasses: dangerClasses };
};

export const custodianValidator = (custodian: string): object => {
  if (!isEmpty(custodian, { ignore_whitespace: true })) {
    return { valid: true, custodianClasses: successClasses };
  }
  return { valid: false, custodianClasses: dangerClasses };
};

export const contactOrgValidator = (contact: string): object => {
  if (!isEmpty(contact, { ignore_whitespace: true })) {
    return { valid: true, contactOrganisationClasses: successClasses };
  }
  return { valid: false, contactOrganisationClasses: dangerClasses };
};

export const contactPositionValidator = (contact: string): object => {
  if (!isEmpty(contact, { ignore_whitespace: true })) {
    return { valid: true, contactPositionClasses: successClasses };
  }
  return { valid: false, contactPositionClasses: dangerClasses };
};

export const storedFormatValidator = (storedFormat: string): object => {
  if (storedFormat) {
    return { valid: true, storedFormatClasses: successClasses };
  }
  return { valid: false, storedFormatClasses: dangerClasses };
};

export const availableFormatsValidator = (availableFormats: string): object => {
  if (availableFormats === null || availableFormats.length === 0) {
    return { valid: false, availableFormatsClasses: dangerClasses };
  } else {
    return { valid: true, availableFormatsClasses: successClasses };
  }
};

export const accessRightsValidator = (accessRights: string): object => {
  if (accessRights) {
    return { valid: true, accessRightsClasses: successClasses };
  }
  return { valid: false, accessRightsClasses: dangerClasses };
};

export const useRestrictionsValidator = (useRestrictions: string): object => {
  if (!isEmpty(useRestrictions, { ignore_whitespace: true })) {
    return { valid: true, useRestrictionsClasses: successClasses };
  }
  return { valid: false, useRestrictionsClasses: dangerClasses };
};

export const securityClassificationValidator = (securityClassification: string): object => {
  if (securityClassification) {
    return { valid: true, securityClassificationClasses: successClasses };
  }
  return { valid: false, securityClassificationClasses: dangerClasses };
};

export const generalisationsValidator = (generalisations: string): object => {
  if (!isEmpty(generalisations, { ignore_whitespace: true })) {
    return { valid: true, generalisationsClasses: successClasses };
  }
  return { valid: false, generalisationsClasses: dangerClasses };
};

export const dataAccessRequestDOIValidator = (dataAccessRequestDOI: string) => {
  if (dataAccessRequestDOI && dataAccessRequestDOI.match(doiRegex)) {
    return { valid: true, dataAccessRequestDOIClasses: successClasses };
  } else {
    return { valid: false, dataAccessRequestDOIClasses: dangerClasses };
  }
};

export const orcIDValidator = (orcID: string | undefined) => {
  if (orcID === undefined) {
    return false;
  } else {
    return !isEmpty(orcID, { ignore_whitespace: true });
  }
};

export function notifyError(message: string): void {
  const { oruga } = useProgrammatic();
  oruga.notification.open({
    variant: 'danger',
    message: message,
    position: 'top',
    duration: 5000,
    closable: true,
  });
}

export const abstractValidator = (abstract: string): object => {
  const abstractValid = !isEmpty(abstract, { ignore_whitespace: true });
  if (abstractValid) {
    return { valid: abstractValid, abstractClasses: successClasses };
  }
  return { valid: abstractValid, abstractClasses: dangerClasses };
};
