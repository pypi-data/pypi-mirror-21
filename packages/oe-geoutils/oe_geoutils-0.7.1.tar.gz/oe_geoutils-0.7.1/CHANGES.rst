0.7.1 (12-04-2017)
------------------

- Location elements fix #18


0.7.0 (29-03-2017)
------------------

- Update vlaams_gewest + add default tolerance value (10 meters) in check_within_flanders


0.6.0 (01-03-2017)
------------------

- Locatie component centraliseren #14 

0.5.3 (08-02-2017)
------------------

- check_erfgoedgemeente python3 compatible

0.5.2 (19-12-2016)
------------------

- changed check on alpha_2 as pycountry.countries key

0.5.1 (12-12-2016)
------------------

- added alpha_2 as a pycountry.countries key

0.5.0 (08-12-2016)
------------------

- location element validation (#11)

0.4.1 (21-11-2016)
------------------

- capakey validation with regex (#9)
- bring tests up to date

0.4.0 (13-09-2016)
------------------

- Adding "check_in_erfgoedgemeente" endpoint and util function".

0.3.0 (05-09-2016)
------------------

- Adding "/gemeente" and "/provincie" endpoints.

0.2.9 (01-07-2016)
------------------

- Making contour geometry valid with buffer of 0 meters instead of union.

0.2.8 (24-06-2016)
------------------

- Updating validation contour: bugfix.

0.2.7 (24-06-2016)
------------------

- Updating validation contour: remove duplicate consecutive coordinates (OGC SFA en ISO 19107:2003 standard).

0.2.6 (02-06-2016)
------------------

- Updating AdminGrenzenClient: get administrative areas by POST (not GET).

0.2.5 (26-04-2016)
------------------

- Adding function which returns the provinces intersecting with the input geojson.

0.2.4 (21-04-2016)
------------------

- Adding function which returns the province that has the largest intersecting area with the input geojson.

0.2.3 (12-04-2016)
------------------

- Including `crabpy` modules.


0.2.2 (07-04-2016)
------------------

- Adding `check_within_flanders` endpoint.


0.2.1 (05-04-2016)
------------------

- "gemeente" attribute as an encoded value.


0.2.0 (01-04-2016)
------------------

- Extending output nearest address when success with a boolean attribute "found" and an "address" attribute if "found" is true.


0.1.1 (23-03-2016)
------------------

- Extending contour validator: A self-intersecting MultiPolygon will be unified.


0.1.0 (04-03-2016)
------------------

-  Initial version

