class incident:
    def _init_(self,report_id,date,airport,aircraft_id,aircraft_type,pilot_percent_hours_type,pilot_total_hours,midair,narrative=''):
        assert len(report_id) >= 8 and len(report_id.split())==1,'invalid report_id'
        self._report_id=report_id
        self.date=date
        self.airport=airport
        self.aircraft_id=aircraft_id
        self.aircraft_type=aircraft_type
        self.pilot_percent_hours_type=pilot_percent_hours_type
        self.pilot_total_hours=pilot_total_hours
        self.midair=midair
        self.narrative=narrative

@property
def date(self):
    return self._date
@date.setter
def date(self,date):
    assert isinstance(date,datetime.date),'invalid date'
    self._date=date

    
class IncidentCollection(dict):
    def values(self):
        for report_id in self.keys()
            yield self[report_id]
    def items(self):
        for report_id in self.keys():
            yield(report_id,self[report_id])
    def _iter_(self):
        for report_id in sorted(super().keys()):
            yield report_id
    keys=_iter_