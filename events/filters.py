import django_filters
from .models import Event
from django import forms

class EventFilter(django_filters.FilterSet):

    STATE_DICT = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }
    states = [(state, state) for state in STATE_DICT.keys()]
    skill_levels = [(skill, skill) for skill in ['Beginner','Intermediate','Advanced']]

    event_state = django_filters.ChoiceFilter(label='Location', 
                                              choices=states, 
                                              method='filter_by_state', 
                                              widget=forms.Select(attrs={'class' : 'form-control-sm'}, choices=states))
    skill_level = django_filters.ChoiceFilter(label='Skill Level', 
                                              choices=skill_levels, 
                                              method='filter_by_skill_level', 
                                              widget=forms.Select(attrs={'class' : 'form-control-sm'}, choices=skill_levels))
    charge_length = django_filters.NumberFilter(label='Max Ride Distance (Miles)',
                                                lookup_expr='lte',
                                                field_name='continuous_charge_miles_needed',
                                                widget=forms.NumberInput(attrs={'class' : 'form-control-sm w-25'}))
    
    # class Meta:
    #     model = Event
    #     #for exact match
    #     # fields = ['title] 
    #     fields = {
    #         #this is the syntax needed for not-exact match filtering
    #         'title' : ['icontains'] 
    #     }

    def filter_by_state(self, queryset, name, value):
        return queryset.filter(formatted_address__contains=self.STATE_DICT[value])
    def filter_by_skill_level(self, queryset, name, value):
        return queryset.filter(skill_level=value)

