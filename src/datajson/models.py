from pydantic import BaseModel, Field 
from enum import Enum
from typing import Optional


class AccrualPeriodicity(Enum):
    '''
    Values for 'accrualPeriodicity' field
    '''

    RP_10Y = 'R/P10Y'
    RP_4Y = 'R/P4Y'
    RP_1Y = 'R/P1Y'
    RP_2M = 'R/P2M' 
    RP_2_W ='R/P0.5W'
    RP_1D = 'R/P1D'
    RP_2X_M = 'R/P2M'
    RP_6M = 'R/P6M'
    RP_2Y = 'R/P2Y'
    RP_3Y = 'R/P3Y'
    RP_3X_W = 'R/P0.33W'
    RP_3X_M = 'R/P0.33M'
    RP_CONT = 'R/PT1S'
    RP_1M = 'R/P1M'
    RP_1Q = 'R/P3M'
    RP_3X_Y = 'R/P4M'
    RP_1W = 'R/P1W'
    RP_1H	= 'R/PT1H'

    @property
    def description(self) -> str:
        return {
            'RP_10Y': 'published every 10 years', 
            'RP_4Y': 'published every 4 years', 
            'RP_1Y': 'published 1 time per year', 
            'RP_2M': 'published every other month', 
            'RP_2_W': 'published 2 times per week', 
            'RP_1D': 'published daily', 
            'RP_2X_M': 'published every other week', 
            'RP_6M': 'published twice per year, every 6 months', 
            'RP_2Y': 'published every 2 years', 
            'RP_3Y': 'published every 3 years', 
            'RP_3X_W': 'published 3 times each week', 
            'RP_3X_M': 'published 3 times each month', 
            'RP_CONT': 'updated continously', 
            'RP_1M': 'published 1 time per month', 
            'RP_1Q': 'published once each quarter, 4 times per year', 
            'RP_3X_Y': 'published 3 times each year', 
            'RP_1W': 'published 1 time per week', 
            'RP_1H': 'published 1 time per hour'
        }[self.value]


class DataTheme(Enum): 
    '''
    Values for 'themes' field
    '''

    eligibility = 'Eligibility'
    drug_pricing_payment = 'Drug Pricing and Payment'
    enrollment = 'Enrollment'
    national_average_drug_cost = 'National Average Drug Acqusition Cost'
    quality = 'Quality'
    state_drug_utilization = 'State Drug Utilization'
    uncategorized = 'Uncategorized'
    unwinding = 'Unwinding'



class BureauCode(Enum):
    '''
    Values for 'bureauCode' field
    '''

    HHS = '009:00'
    CMS = '009:38'

    @classmethod 
    def get_full_name(cls, code:str) -> str:
        "Get the full name of an agency from its bureau code"

        full_names = {
            'HHS': 'Department of Health and Human Services', 
            'CMS': 'Centers for Medicare and Medicaid Services'
        }


        return full_names.get(code, code)


class SearchParams(BaseModel):
    keyword:Optional[str] = Field(None, description='keywords that describe the dataset')
    theme:Optional[DataTheme] = Field(None, description='themes that describe the dataset')
    description:Optional[str] = Field(None, description='dataset description')
    bureauCode:Optional[BureauCode] = Field(None, description='indicates what agency/bureau the data is from')
    periodicity:Optional[AccrualPeriodicity] = Field(None, description='how frequently the data is updated')
    size:Optional[int] = Field(10, description='number of results to return')


    def to_url(self) -> dict[str]: 
        '''
        convert parameters to search URL
        '''
        criteria = {}

        if self.keyword:
            criteria['keyword'] = self.keyword

        if self.theme:
            criteria['theme'] = self.theme 

        if self.description:
            criteria['description'] = self.description

        if self.bureauCode:
            criteria['bureauCode'] = self.bureauCode

        if self.periodicity:
            criteria['accrualPeriodicity'] = self.periodicity

        if len(criteria) != 0:
            return criteria
        