CREATE INDEX area_airport_id_index
ON AREA(airport_id);

CREATE INDEX runway_in_airport_index
ON RUNWAY(AIRPORT_ID);

CREATE INDEX flight_controller_for_runway_index
ON FLIGHT_CONTROLLER(RUNWAY_ID);

CREATE INDEX log_managed_by_airport_index
ON LOGS(managed_by);

CREATE INDEX airlinecompany_personnel_p_key
ON airlinecompany_personnel(personnel_key);

CREATE INDEX parking_slot_flight_kay_index
ON parking_slot(flight_key);

CREATE INDEX airplane_type_crew_key
ON airplane_type(crew_key);

CREATE INDEX airplane_type_key
ON airplane(type_key);

CREATE INDEX crew_employeeonboard_personnel_key
ON crew_employeeonboard(personnel_key);

CREATE INDEX flightsegment_airplanetype_flight_segment_key
ON flightsegment_airplanetype(flight_segment_key);

CREATE INDEX technicalissue_airplane_tdate
ON technicalissue_airplane(tdate);


