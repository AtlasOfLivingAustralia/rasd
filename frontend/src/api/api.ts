import axios, { AxiosError } from 'axios';
import type {
  ApiError,
  ApiPaginatedResults,
  ApiPaginatedResponse,
  ApiResponse,
  Registration,
  WhoAmIData,
  DataAccessRequestWrite,
  DatasetRequest,
  DatasetRequestAudit,
  DataAccessRequestRead,
  OrganisationState,
  PublicDataAccessRequestRead,
  PublicDatasetRequest,
} from '@/api/api.types';
import { DateTime } from 'luxon';
import isEmpty from 'validator/es/lib/isEmpty';
import { fetchUserData, useUserDataStore } from '@/store';
import type { AccessRequestEnumType } from '@/api/api.types';
import { DatasetAction, UserGroup } from '@/api/api.types';
import { orcIDValidator } from '@/helpers/helpers';
import * as interceptors from '@/api/interceptors';

// set axios base API url
let base_api_url = import.meta.env.VITE_API_BASE_URL;
// remove trailer slash if any. Let us prefix the slash in axios urls.
if (base_api_url.endsWith('/')) {
  base_api_url = base_api_url.slice(0, -1);
}
axios.defaults.baseURL = base_api_url;
// register interceptors
axios.interceptors.response.use(null, interceptors.catchAuthError);

export function setAuthHeader(token: string): void {
  if (token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    removeAuthHeader();
  }
}
export function removeAuthHeader(): void {
  delete axios.defaults.headers.common['Authorization'];
}

// URL params without the guff
export function stripNullParams<T extends object>(params: T): Record<string, string> {
  return Object.fromEntries(
    Object.entries(params).filter(([, value]) => {
      return typeof value !== 'undefined' && value != null;
    })
  );
}

// Authentication API Calls
export const loginAPI = async function login(username: string, password: string) {
  let message: [string, boolean] | [];
  const userStore = useUserDataStore();
  await axios
    .post(
      '/auth/login',
      {
        username: username,
        password: password,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(async function (response) {
      message = ['Login successful', true];
      const idToken = response.data.IdToken;
      setAuthHeader(idToken);
      userStore.setIdToken(idToken);
      // the login is considered complete only if we can get all user information and push the user data in the store
      // for that we use the store fetchUserData.
      await fetchUserData().catch(function (error: unknown) {
        if (error instanceof Error) {
          message = [error.message, false];
        } else {
          message = ['Unable to retrieve user data.', false];
        }
      });
    })
    .catch(function (error) {
      console.log('Login error:', error);
      console.log('Error response:', error.response);
      console.log('Error response data:', error.response?.data);
      const detail = error.response?.data?.detail || 'Invalid email address or password';
      console.log('Detail:', detail);
      if (detail.includes('PasswordResetRequiredException') || detail.includes('Password reset required')) {
        message = ['PASSWORD_EXPIRED', false];
      } else {
        message = [detail, false];
      }
    });
  // @ts-ignore
  return message;
};

export const whoAmIAPI = async function whoAmI(): Promise<ApiResponse<WhoAmIData>> {
  let userData: WhoAmIData | undefined;
  let error: ApiError | undefined;
  const userStore = useUserDataStore();
  if (userStore.isLoggedIn) {
    await axios
      .get('/auth/whoami', {
        headers: {
          'Content-Type': 'application/json',
        },
      })
      .then(function (response) {
        userData = {
          id: response.data.id,
          email: response.data.email,
          familyName: response.data.family_name,
          givenName: response.data.given_name,
          groups: response.data.groups,
          organisationId: response.data.organisation_id,
        };
      })
      .catch(function (e) {
        if (e instanceof Error) {
          error = {
            message: e.message,
            detail: [],
          };
          if (e instanceof AxiosError) {
            error.code = e.code;
            error.status = e.response?.status;
            error.statusText = e.response?.statusText;
          }
        }
      });
  }
  return { data: userData, error };
};

export const createPasswordAPI = async function createPassword(
  username: string,
  temp_password: string,
  new_password: string
) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/auth/password/set',
      {
        username: username,
        temp_password: temp_password,
        new_password: new_password,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(() => {
      message = ['Your password has been set', true];
    })
    .catch((error) => {
      message = [error.response.data.detail, false];
    });
  // @ts-ignore
  return message;
};

export const forgotPasswordAPI = async function forgotPassword(username: string) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/auth/password/forgot',
      {
        username: username,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(() => {
      message = [`An email has been sent to ${username}. Please check your inbox`, true];
    })
    .catch((error) => {
      message = [error.response.data.detail, false];
    });
  // @ts-ignore
  return message;
};

export const checkUserStatusAPI = async function checkUserStatus(username: string): Promise<boolean> {
  try {
    const response = await axios.get(`/auth/user-status/${username}`);
    return response.data.needsTempPassword || false;
  } catch (error) {
    console.error('Error checking user status:', error);
    return false;
  }
};

export const resendTempPasswordAPI = async function resendTempPassword(username: string) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/auth/password/resend-temp',
      {
        username: username,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(() => {
      message = [`Temporary password has been resent to ${username}`, true];
    })
    .catch((error) => {
      message = [error.response?.data?.detail || 'Failed to resend temporary password', false];
    });
  // @ts-ignore
  return message;
};

export const confirmForgotPasswordAPI = async function confirmForgotPassword(
  username: string,
  code: string,
  new_password: string
) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/auth/password/forgot/confirm',
      {
        username: username,
        code: code,
        password: new_password,
      },
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      }
    )
    .then(() => {
      message = ['Your password has been reset', true];
    })
    .catch((error) => {
      message = [error.response.data.detail, false];
    });
  // @ts-ignore
  return message;
};

//Will need to flesh out error handling to report messages to the user but this will do for now.
export const createOrganisationAPI = async function createOrganisation(name: string, abn: string, email: string) {
  let message: (string | boolean)[];

  await axios
    .post(
      '/organisations',
      {
        name: name,
        abn: abn,
        email: email,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then(() => {
      message = ['Your Organisation has been created!', true];
    })
    .catch(() => {
      message = [
        'There has been a problem adding your organisation. The ABN may be inactive or you may already be registered.',
        false,
      ];
    });
  // @ts-ignore
  return message;
};

export const getOrganisationsAPI = async function getOrganisations() {
  let organisations: any[] = [];
  await axios
    .get('/organisations')
    .then((response) => {
      organisations = response.data.results;
    })
    .catch(() => {
      organisations = [];
    });
  return organisations;
};

export const getOrganisationAPI = async function getOrganisation(id: string): Promise<OrganisationState | undefined> {
  let organisation: OrganisationState | undefined;
  // const organisationDataStore = useOrganisationDataStore();
  await axios.get('/organisations/' + id).then((response) => {
    organisation = response.data;
  });
  return organisation;
};

export const editOrganisationAPI = async function editOrganisation(id: string, email: string) {
  let message: (string | boolean)[];
  await axios
    .patch(
      '/organisations/' + id,
      {
        email: email,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then(() => {
      message = ['Your Organisation has been updated!', true];
    })
    .catch(() => {
      message = ['There was a problem updating your organisation.', false];
    });
  // @ts-ignore
  return message;
};

export const createMetadataAPI = async function createMetadata(
  title: string,
  abstract: string,
  keywords: [],
  temporal_coverage_from: string,
  temporal_coverage_to: string,
  north_bounding_coordinate: number,
  south_bounding_coordinate: number,
  east_bounding_coordinate: number,
  west_bounding_coordinate: number,
  locations: [],
  taxa_covered: string,
  collection_methods: [],
  data_source_url: string,
  data_source_doi: string,
  embargoed: boolean,
  embargo_release_date: string,
  contact_organisation: string,
  contact_position: string,
  contact_email: string,
  stored_format: string,
  available_formats: [],
  access_rights: string,
  use_restrictions: string,
  security_classification: string,
  generalisations: string
) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/metadata',
      {
        title: title,
        abstract: !isEmpty(abstract, { ignore_whitespace: true }) ? abstract : null,
        keywords: keywords,
        temporal_coverage_from: temporal_coverage_from,
        temporal_coverage_to: temporal_coverage_to,
        north_bounding_coordinate: north_bounding_coordinate,
        south_bounding_coordinate: south_bounding_coordinate,
        east_bounding_coordinate: east_bounding_coordinate,
        west_bounding_coordinate: west_bounding_coordinate,
        locations: locations,
        taxa_covered: taxa_covered,
        collection_methods: collection_methods,
        data_source_url: !isEmpty(data_source_url, { ignore_whitespace: true }) ? data_source_url : null,
        data_source_doi: !isEmpty(data_source_doi, { ignore_whitespace: true }) ? data_source_doi : null,
        embargoed: embargoed,
        embargo_release_date: embargo_release_date,
        contact_organisation: contact_organisation,
        contact_position: contact_position,
        contact_email: contact_email,
        stored_format: stored_format,
        available_formats: available_formats,
        access_rights: access_rights,
        use_restrictions: use_restrictions,
        security_classification: security_classification,
        generalisations: generalisations,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then(() => {
      message = ['Your Metadata has been created!', true];
    })
    .catch(() => {
      message = ['There has been a problem creating your metadata.', false];
    });
  // @ts-ignore
  return message;
};

export const getMetadataListAPI = async function getMetadata(limit: number = 20, pageCursor: string = '') {
  let metadata: any[] = [];
  let paramsString = '?active_only=true&limit=' + limit;
  if (pageCursor !== '') {
    paramsString += '&cursor=' + pageCursor;
  }
  await axios
    .get(`/metadata${paramsString}`)
    .then((response) => {
      metadata = response.data;
    })
    .catch(() => {
      metadata = [];
    });
  return metadata;
};

export const getMetadataSearchAPI = async function getMetadata(
  limit: number = 20,
  pageCursor: string = '',
  keyword: [] = [],
  locations: [] = [],
  title: string = '',
  description: string = '',
  organisation: string = ''
) {
  let metadata: any[] = [];
  let paramsString = '?active_only=true&limit=' + limit;
  if (pageCursor !== '') {
    paramsString += '&cursor=' + pageCursor;
  }
  if (keyword.length > 0) {
    keyword.map((key) => (paramsString += '&keywords=' + key));
  }
  if (locations.length > 0) {
    locations.map((key) => (paramsString += '&locations=' + key));
  }
  if (title !== '') {
    paramsString += '&title=' + title;
  }
  if (description !== '') {
    paramsString += '&abstract=' + description;
  }
  if (organisation !== '') {
    paramsString += '&organisation_id=' + organisation;
  }
  await axios
    .get(`/metadata/search${paramsString}`)
    .then((response) => {
      metadata = response.data;
    })
    .catch(() => {
      metadata = [];
    });
  return metadata;
};

export const getMetadataAPI = async function getMetadata(id: string) {
  let metadata: any;
  await axios
    .get('/metadata/' + id)
    .then((response) => {
      metadata = response.data;
    })
    .catch(() => {
      metadata = {};
    });
  return metadata;
};

export const editMetadataAPI = async function editMetadata(
  id: string,
  title: string,
  abstract: string,
  keywords: [],
  temporal_coverage_from: string,
  temporal_coverage_to: string,
  north_bounding_coordinate: number,
  south_bounding_coordinate: number,
  east_bounding_coordinate: number,
  west_bounding_coordinate: number,
  locations: string,
  taxa_covered: string,
  collection_methods: [],
  data_source: string,
  embargoed: boolean,
  embargo_release_date: string,
  custodian: string,
  contact_organisation: string,
  contact_position: string,
  contact_email: string,
  stored_format: string,
  available_formats: [],
  access_rights: string,
  use_restrictions: string,
  security_classification: string,
  generalisations: string
) {
  let message: (string | boolean)[];
  await axios
    .patch(
      '/metadata/' + id,
      {
        title: title,
        abstract: !isEmpty(abstract, { ignore_whitespace: true }) ? abstract : null,
        keywords: keywords,
        temporal_coverage_from: temporal_coverage_from,
        temporal_coverage_to: temporal_coverage_to,
        north_bounding_coordinate: north_bounding_coordinate,
        south_bounding_coordinate: south_bounding_coordinate,
        east_bounding_coordinate: east_bounding_coordinate,
        west_bounding_coordinate: west_bounding_coordinate,
        locations: locations,
        taxa_covered: taxa_covered,
        collection_methods: collection_methods,
        data_source: data_source,
        embargoed: embargoed,
        ...(embargo_release_date !== null && { embargo_release_date: embargo_release_date }),
        custodian: custodian,
        contact_organisation: contact_organisation,
        contact_position: contact_position,
        contact_email: contact_email,
        stored_format: stored_format,
        available_formats: available_formats,
        access_rights: access_rights,
        use_restrictions: use_restrictions,
        security_classification: security_classification,
        generalisations: generalisations,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then(() => {
      message = ['Your Metadata has been updated!', true];
    })
    .catch(() => {
      message = ['There has been a problem updating your metadata.', false];
    });
  // @ts-ignore
  return message;
};

export const getAccessRightsAPI = async function getAccessRights() {
  let accessRights: any[] = [];
  await axios
    .get('/metadata/access-rights')
    .then((response) => {
      accessRights = response.data;
    })
    .catch(() => {
      accessRights = [];
    });
  return accessRights;
};

export const getCollectionMethodsAPI = async function getCollectionMethods() {
  let collectionMethods: any[] = [];
  await axios
    .get('/metadata/collection-methods')
    .then((response) => {
      collectionMethods = response.data;
    })
    .catch(() => {
      collectionMethods = [];
    });
  return collectionMethods;
};

export const getFormatsAPI = async function getFormats() {
  let formats: any[] = [];
  await axios
    .get('/metadata/formats')
    .then((response) => {
      formats = response.data;
    })
    .catch(() => {
      formats = [];
    });
  return formats;
};

export const getKeywordsAPI = async function getKeywords() {
  let keywords: string[] | undefined;
  await axios
    .get('/metadata/keywords')
    .then((response) => {
      keywords = response.data;
    })
    .catch(() => {
      keywords = [];
    });
  return keywords;
};

export const getLocationsAPI = async function getLocations() {
  let locations: string[] | undefined;
  await axios
    .get('/metadata/locations')
    .then((response) => {
      locations = response.data;
    })
    .catch(() => {
      locations = [];
    });
  return locations;
};

export const getSecurityClassificationsAPI = async function getSecurityClassifications() {
  let securityClassifications: any[] = [];
  await axios
    .get('/metadata/security-classifications')
    .then((response) => {
      securityClassifications = response.data;
    })
    .catch(() => {
      securityClassifications = [];
    });
  return securityClassifications;
};

export const lookupABNAPI = async function lookupABN(abn: string) {
  let organisation: any;
  await axios
    .get('/abn/lookup/' + abn)
    .then((response) => {
      organisation = response.data;
    })
    .catch(() => {
      organisation = {};
    });
  return organisation;
};

export const registerAPI = async function register(
  username: string,
  given_name: string,
  family_name: string,
  group: string,
  organisation: string | object,
  agreements: string[]
) {
  let message: (string | boolean)[];
  await axios
    .post(
      '/register',
      {
        username: username,
        given_name: given_name,
        family_name: family_name,
        group: group,
        organisation: organisation,
        agreements: agreements,
      },
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    )
    .then(() => {
      message = ['Your registration request has been received! The RASD team will be in touch.', true];
    })
    .catch(() => {
      message = ['There has been a problem sending your registration request.', false];
    });
  // @ts-ignore
  return message;
};

export async function getRegistrationsAPI(
  limit: number,
  cursor: string | undefined,
  status: string | undefined
): Promise<ApiPaginatedResponse<Registration>> {
  const params = stripNullParams({ limit, cursor, status });
  let data: ApiPaginatedResults<Registration> | undefined;
  let error: ApiError | undefined;

  try {
    const response = await axios.get('/register?' + new URLSearchParams(params), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    data = {
      cursor: response.data.cursor,
      count: response.data.count,
      results: response.data.results.map((result: Record<string, unknown>) => {
        return {
          active: result.active,
          id: result.id,
          username: result.username,
          givenName: result.given_name,
          familyName: result.family_name,
          group: result.group,
          organisation: result.organisation,
          agreements: result.agreements,
          status: result.status,
          reason: result.reason,
          organisationOverride: result.organisation_override,
          actionedBy: result.actioned_by,
          createdAt: result.created_at, // Store as ISO string for correct sorting
        } as Registration;
      }),
    };
  } catch (e) {
    if (e instanceof Error) {
      error = {
        message: e.message,
      };

      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
      }
    }
  }
  return { data, error };
}

export async function approveRequestAPI(id: string, approve: boolean) {
  let data: boolean | undefined;
  let error: ApiError | undefined;

  try {
    await axios.post(`/register/${id}/${approve ? 'approve' : 'decline'}`);
    data = true;
  } catch (e) {
    if (e instanceof Error) {
      error = {
        message: e.message,
      };

      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
      }
    }
  }

  return { data: data, error };
}

export async function submitAccessRequestAPI(accessRequest: DataAccessRequestWrite) {
  const requestData = stripNullParams({
    metadata_ids: accessRequest.metadataIds,
    requestor_organisation_address: accessRequest.organisationAddress,
    requestor_organisation_indigenous_body: accessRequest.isIndigenousOrg,
    ...(orcIDValidator(accessRequest.orcId) && { requestor_orcid: accessRequest.orcId }),
    project_title: accessRequest.projectTitle,
    project_purpose: accessRequest.purpose,
    project_research: accessRequest.researchTopic,
    project_industry: accessRequest.industryType,
    project_commercial: accessRequest.commercialPurposes,
    project_public_benefit_explanation: accessRequest.publicBenefit,
    data_requested: accessRequest.dataRequested,
    data_relevance_explanation: accessRequest.dataRelevance,
    data_frequency: accessRequest.frequency,
    data_required_from: accessRequest.dateRequiredFrom
      ? DateTime.fromJSDate(accessRequest.dateRequiredFrom).toFormat('yyyy-MM-dd')
      : undefined,
    data_required_to: accessRequest.dateRequiredTo
      ? DateTime.fromJSDate(accessRequest.dateRequiredTo).toFormat('yyyy-MM-dd')
      : undefined,
    data_frequency_explanation: accessRequest.requiredPeriod,
    data_area: accessRequest.requiredArea,
    data_area_explanation: accessRequest.boundingBox,
    data_security_explanation: accessRequest.securityControls,
    data_access: accessRequest.userAccess,
    data_access_explanation: accessRequest.groupAccessName,
    data_distribution_explanation: accessRequest.distributedTo,
    data_accept_transformed: accessRequest.willAcceptTransformed,
  });

  let data: { id: string } | undefined;
  let error: ApiError | undefined;

  try {
    const response = await axios.post('/access-requests?', requestData, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    data = { id: response.data.id };
  } catch (e) {
    if (e instanceof Error) {
      error = {
        message: e.message,
      };

      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
        error.detail = e.response?.data.detail;
      }
    }
  }
  return { data, error };
}

export async function lookupAccessRequestEnumAPI(
  accessRequestEnumType: AccessRequestEnumType
): Promise<ApiResponse<string[]>> {
  let data: string[] | undefined;
  let error: ApiError | undefined;

  try {
    const response = await axios.get(`/access-requests/${accessRequestEnumType}`, {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    data = response.data;
  } catch (e) {
    if (e instanceof Error) {
      error = {
        message: e.message,
      };

      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
      }
    }
  }
  return { data, error };
}

export async function getAccessRequestsAPI(
  role: UserGroup.DataCustodians | UserGroup.DataRequestors | UserGroup.Administrators | undefined,
  limit: number,
  cursor: string | undefined
): Promise<ApiPaginatedResponse<DataAccessRequestRead>> {
  const params = stripNullParams({ limit, cursor });
  let rolePath: string | undefined;
  switch (role) {
    case UserGroup.DataCustodians:
      rolePath = 'custodian';
      break;
    case UserGroup.DataRequestors:
      rolePath = 'requestor';
      break;
    case UserGroup.Administrators:
      rolePath = 'administrator';
      break;
    default:
      rolePath = undefined;
  }

  let data: ApiPaginatedResults<DataAccessRequestRead> | undefined;
  let error: ApiError | undefined;
  const url = rolePath === 'administrator' ? `/access-requests?` : `/access-requests/${rolePath}?`;
  try {
    const response = await axios.get(url + new URLSearchParams(params), {
      headers: {
        'Content-Type': 'application/json',
      },
    });
    data = {
      cursor: response.data.cursor,
      count: response.data.count,
      results: response.data.results.map((result: Record<string, unknown>) => {
        return {
          active: result.active,
          id: result.id,
          completed_at: result.completed_at,
          doi: result.doi,
          isDOIEditable: false,
          datasetRequests: (result.dataset_requests as Record<string, unknown>[]).map(
            (rawDatasetRequest) =>
              ({
                active: rawDatasetRequest.active,
                id: rawDatasetRequest.id,
                status: rawDatasetRequest.status,
                metadataId: rawDatasetRequest.metadata_id,
                metadataTitle: rawDatasetRequest.metadata_title,
                custodianId: rawDatasetRequest.custodian_id,
                custodianName: rawDatasetRequest.custodian_name,
                custodianEmail: rawDatasetRequest.custodian_email,
                legalAgreementSigned: false,
                audit: rawDatasetRequest.audit as DatasetRequestAudit[],
              } as DatasetRequest)
          ),
          custodianIds: result.custodianIds,
          requestor: {
            id: result.requestor_id,
            givenName: result.requestor_given_name,
            familyName: result.requestor_family_name,
            email: result.requestor_email,
            organisationId: result.requestor_organisation_id,
            organisationName: result.requestor_organisation_name,
            organisationEmail: result.requestor_organisation_email,
            organisationAddress: result.requestor_organisation_address,
            organisationIndigenousBody: result.requestor_organisation_indigenous_body,
            orcid: result.requestor_orcid,
          },
          project: {
            title: result.project_title,
            purpose: result.project_purpose,
            research: result.project_research,
            industry: result.project_industry,
            commercial: result.project_commercial,
            publicBenefitExplanation: result.project_public_benefit_explanation,
          },
          data: {
            requested: result.data_requested,
            relevanceExplanation: result.data_relevance_explanation,
            frequency: result.data_frequency,
            requiredFrom: result.data_required_from,
            requiredTo: result.data_required_to,
            frequencyExplanation: result.data_frequency_explanation,
            area: result.data_area,
            areaExplanation: result.data_area_explanation,
            securityExplanation: result.data_security_explanation,
            access: result.data_access,
            accessExplanation: result.data_access_explanation,
            distributionExplanation: result.data_distribution_explanation,
            acceptTransformed: result.data_accept_transformed,
          },
        } as DataAccessRequestRead;
      }),
    };
  } catch (e) {
    if (e instanceof Error) {
      error = {
        message: e.message,
      };

      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
      }
    }
  }
  return { data, error };
}

export async function getAccessRequestsSearchAPI(
  role: UserGroup.DataCustodians | UserGroup.DataRequestors | UserGroup.Administrators | undefined,
  id: string | undefined
): Promise<ApiPaginatedResponse<DataAccessRequestRead>> {
  let error: ApiError | undefined;
  let data: any;
  return axios
    .get(`/access-requests/` + id, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      data = {
        results: {
          active: response.data.active,
          id: response.data.id,
          completed_at: response.data.completed_at,
          doi: response.data.doi,
          isDOIEditable: false,
          datasetRequests: (response.data.dataset_requests as Record<string, unknown>[]).map(
            (rawDatasetRequest) =>
              ({
                active: rawDatasetRequest.active,
                id: rawDatasetRequest.id,
                status: rawDatasetRequest.status,
                metadataId: rawDatasetRequest.metadata_id,
                metadataTitle: rawDatasetRequest.metadata_title,
                custodianId: rawDatasetRequest.custodian_id,
                custodianName: rawDatasetRequest.custodian_name,
                custodianEmail: rawDatasetRequest.custodian_email,
                legalAgreementSigned: false,
                audit: rawDatasetRequest.audit as DatasetRequestAudit[],
              } as DatasetRequest)
          ),
          custodianIds: response.data.custodianIds,
          requestor: {
            id: response.data.requestor_id,
            givenName: response.data.requestor_given_name,
            familyName: response.data.requestor_family_name,
            email: response.data.requestor_email,
            organisationId: response.data.requestor_organisation_id,
            organisationName: response.data.requestor_organisation_name,
            organisationEmail: response.data.requestor_organisation_email,
            organisationAddress: response.data.requestor_organisation_address,
            organisationIndigenousBody: response.data.requestor_organisation_indigenous_body,
            orcid: response.data.requestor_orcid,
          },
          project: {
            title: response.data.project_title,
            purpose: response.data.project_purpose,
            research: response.data.project_research,
            industry: response.data.project_industry,
            commercial: response.data.project_commercial,
            publicBenefitExplanation: response.data.project_public_benefit_explanation,
          },
          data: {
            requested: response.data.data_requested,
            relevanceExplanation: response.data.data_relevance_explanation,
            frequency: response.data.data_frequency,
            requiredFrom: response.data.data_required_from,
            requiredTo: response.data.data_required_to,
            frequencyExplanation: response.data.data_frequency_explanation,
            area: response.data.data_area,
            areaExplanation: response.data.data_area_explanation,
            securityExplanation: response.data.data_security_explanation,
            access: response.data.data_access,
            accessExplanation: response.data.data_access_explanation,
            distributionExplanation: response.data.data_distribution_explanation,
            acceptTransformed: response.data.data_accept_transformed,
          },
        } as DataAccessRequestRead,
      };
      return { data, error };
    })
    .catch((e) => {
      if (e instanceof Error) {
        error = {
          message: e.message,
        };

        if (e instanceof AxiosError) {
          error.code = e.code;
          error.status = e.response?.status;
          error.statusText = e.response?.statusText;
        }
      }
      return { data, error };
    });
}

export async function getAccessRequestsPublicAPI(id: string | null): Promise<ApiResponse<DataAccessRequestRead>> {
  let error: ApiError | undefined;
  let data: any;
  return axios
    .get(`/access-requests/` + id + `/summary`, {
      headers: {
        'Content-Type': 'application/json',
      },
    })
    .then((response) => {
      data = {
        result: {
          id: response.data.id,
          completed_at: response.data.completed_at,
          created_at: response.data.created_at,
          doi: response.data.doi,
          data_frequency: response.data.data_frequency,
          data_required_from: response.data.data_required_from,
          data_required_to: response.data.data_required_to,
          data_frequency_explanation: response.data.data_frequency_explanation,
          data_area: response.data.data_area,
          data_area_explanation: response.data.data_area_explanation,
          data_requested: (response.data.dataset_requests as Record<string, unknown>[]).map(
            (rawDatasetRequest) =>
              ({
                id: rawDatasetRequest.id,
                metadataTitle: rawDatasetRequest.metadata_title,
                custodianName: rawDatasetRequest.custodian_name,
                data_source_doi: rawDatasetRequest.metadata_data_source_doi,
                data_source_url: rawDatasetRequest.metadata_data_source_url,
              } as PublicDatasetRequest)
          ),
        } as PublicDataAccessRequestRead,
      };
      return { data, error };
    })
    .catch((e) => {
      if (e instanceof Error) {
        error = {
          message: e.message,
        };

        if (e instanceof AxiosError) {
          error.code = e.code;
          error.status = e.response?.status;
          error.statusText = e.response?.statusText;
        }
      }
      return { data, error };
    });
}

export async function actionRequestAPI(accessRequestId: string, datasetRequestId: string, action: DatasetAction) {
  let data: { id: string } | undefined;
  let error: ApiError | undefined;

  try {
    const response = await axios.post(
      `/access-requests/${accessRequestId}/dataset-requests/${datasetRequestId}/${action}`
    );
    data = { id: response.data.id };
  } catch (e) {
    if (e instanceof Error) {
      error = { message: e.message };
      if (e instanceof AxiosError) {
        error.code = e.code;
        error.status = e.response?.status;
        error.statusText = e.response?.statusText;
        error.detail = e.response?.data.detail;
      }
    }
  }
  return { data, error };
}

export async function editDataAccessRequestDOIAPI(accessRequestId: string, accessRequestDOI: Promise<string>) {
  let message: [string, boolean] | [];
  try {
    await axios
      .patch(
        `/access-requests/${accessRequestId}`,
        {
          doi: accessRequestDOI,
        },
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      )
      .then(() => {
        message = [`Data access request has been updated. DOI: ${accessRequestDOI}`, true];
      });
  } catch (error) {
    if (error.response && error.response.data && error.response.data.detail) {
      message = [error.response.data.detail, false];
    } else {
      message = ['There was a problem updating your data access request.', false];
    }
  }
  return message!;
}
