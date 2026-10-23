export interface WhoAmIData {
  id: string;
  familyName: string;
  givenName: string;
  email: string;
  organisationId: string;
  groups: UserGroup[];
}

export enum UserGroup {
  DataCustodians = 'DataCustodians',
  DataRequestors = 'DataRequestors',
  Administrators = 'Administrators',
}

export interface ApiResponse<T> {
  error?: ApiError;
  data?: T;
}

export interface ApiPaginatedResults<T> {
  cursor: string;
  count: number;
  results: T[];
}

export interface ApiPaginatedResponse<T> extends ApiResponse<ApiPaginatedResults<T>> {}

export interface ApiError {
  message: string;
  code?: string;
  status?: number;
  statusText?: string;
  detail?: {
    loc: [string, string];
    msg: string;
    type: string;
  }[];
}

export interface CreateOrganisation {
  id?: string;
  name: string;
  abn: string;
  email: string;
}

export interface Registration {
  active: boolean;
  id: string;
  username: string;
  givenName: string;
  familyName: string;
  group: UserGroup;
  organisation: string | CreateOrganisation;
  agreements: string[];
  status: RegistrationStatus;
  reason: string;
  organisationOverride: string;
  actionedBy: string;
  createdAt: string;
}

export enum RegistrationStatus {
  NEW = 'New',
  APPROVED = 'Approved',
  DECLINED = 'Declined',
}

export interface OrganisationState {
  id: string;
  active: boolean;
  abn: string;
  name: string;
  email: string;
}

export interface DataAccessRequestWrite {
  metadataIds: string[];
  organisationAddress?: string;
  isIndigenousOrg?: boolean;
  orcId?: string;
  projectTitle?: string;
  purpose?: Purpose;
  researchTopic?: ResearchClassifications;
  industryType?: IndustryClassifications;
  commercialPurposes?: boolean;
  publicBenefit?: string;
  dataRequested?: string;
  dataRelevance?: string;
  requiredPeriod?: string;
  dateRequiredFrom?: Date;
  dateRequiredTo?: Date;
  frequency?: Frequency;
  requiredArea?: Area;
  boundingBox?: string;
  securityControls?: string;
  userAccess?: UserAccess;
  groupAccessName?: string;
  distributedTo?: string;
  willAcceptTransformed?: boolean;
}

export interface DataAccessRequestRead {
  id: string;
  completed_at: string;
  doi: string;
  isDOIEditable: boolean;
  datasetRequests: DatasetRequest[];
  custodianIds: string[];
  requestor: {
    id: string;
    givenName: string;
    familyName: string;
    email: string;
    organisationId: string;
    organisationName: string;
    organisationEmail: string;
    organisationAddress: string;
    organisationIndigenousBody: boolean;
    orcid: string;
  };
  project: {
    title: string;
    purpose: string;
    research: string;
    industry: string;
    commercial: boolean;
    publicBenefitExplanation: string;
  };
  data: {
    requested: string;
    relevanceExplanation: string;
    frequency: string;
    requiredFrom: string;
    requiredTo: string;
    frequencyExplanation: string;
    area: string;
    areaExplanation: string;
    securityExplanation: string;
    access: string;
    accessExplanation: string;
    distributionExplanation: string;
    acceptTransformed: boolean;
  };
}

export interface PublicDataAccessRequestRead {
  id: string;
  completed_at: string;
  created_at: string;
  doi: string;
  data_frequency: string;
  data_required_from: string;
  data_required_to: string;
  data_frequency_explanation: string;
  data_area: string;
  data_area_explanation: string;
  data_requested: PublicDatasetRequest[];
}

export interface DatasetRequest {
  id: string;
  status: string;
  metadataId: string;
  metadataTitle: string;
  custodianId: string;
  custodianName: string;
  custodianEmail: string;
  legalAgreementSigned: boolean;
  audit: DatasetRequestAudit[];
}

export interface PublicDatasetRequest {
  id: string;
  metadataTitle: string;
  custodianName: string;
  data_source_doi: string;
  data_source_url: string;
}

export interface DatasetRequestAudit {
  action: string;
  by: string;
  at: string;
}

export enum UserAccess {
  JustMe = 'Just me',
  SelectGroup = 'A select group within my organisation / institution',
  EntireOrg = 'My entire organisation / institution',
  Other = 'Other',
}
export enum IndustryClassifications {
  Agriculture = 'Agriculture, Forestry and Fishing',
  Mining = 'Mining',
  Manufacturing = 'Manufacturing',
  Electricity = 'Electricity, Gas, Water and Waste Services',
  Construction = 'Construction',
  Wholesale = 'Wholesale Trade',
  Retail = 'Retail Trade',
  Accommodation = 'Accommodation and Food Services',
  Transport = 'Transport, Postal and Warehousing',
  Information = 'Information, Media and Telecommunications',
  Financial = 'Financial and Insurance Services',
  Rental = 'Rental, Hiring and Real Estate Services',
  Professional = 'Professional, Scientific and Technical Services',
  Administrative = 'Administrative and Support Services',
  Public = 'Public Administration and Safety',
  Education = 'Education and Training',
  Health = 'Health Care and Social Assistance',
  Arts = 'Arts and Recreational Services',
  Other = 'Other Services',
}
export enum ResearchClassifications {
  Education = 'Education',
  Engineering = 'Engineering',
  EnvironmentalSciences = 'Environmental Sciences',
  HealthSciences = 'Health Sciences',
  HistoryHeritage = 'History, Heritage and Archaeology',
  HumanSociety = 'Human Society',
  IndigenousStudies = 'Indigenous Studies',
  ITCompSci = 'Information and Computing Sciences',
  LanguageCommunications = 'Language, Communications and Culture',
  Law = 'Law and Legal Studies',
  Maths = 'Mathematical Sciences',
  Philosophy = 'Philosophy and Religious Studies',
  PhysicalSciences = 'Physical Sciences',
  Psychology = 'Psychology',
}
export enum Area {
  Whole = 'Whole Dataset',
  Specific = 'Specific Area',
}
export enum Frequency {
  Single = 'Single once off',
  Defined = 'Defined period',
  Ongoing = 'Ongoing',
}
export enum Purpose {
  ToDeliver = 'To deliver government services',
  ToInformPolicies = 'To inform government policies and programs',
  ForResearch = 'For Research and development',
  ForCompliance = 'For compliance and / or enforcement activities',
  ForConservation = 'For conservation management',
  ForPlanning = 'For planning approval',
  ForGovernmentGrant = 'For a government-funded grant program',
  ToInformImpactAssessment = 'To inform environmental impact assessment',
  ForLandManagement = 'For land management',
}

export enum AccessRequestEnumType {
  Custodian = 'custodian',
  Requestor = 'requestor',
  Accesses = 'accesses',
  Areas = 'areas',
  Frequencies = 'frequencies',
  IndustryClassifications = 'industry-classifications',
  Purposes = 'purposes',
  ResearchClassifications = 'research-classifications',
}

export enum DatasetAction {
  Acknowledge = 'acknowledge',
  Approve = 'approve',
  Decline = 'decline',
  AgreementSent = 'agreement-sent',
  Complete = 'complete',
}
