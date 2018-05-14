from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from wedsite.conf import settings
from wedsite.models import RSVP, RSVPPerson

import csv
import sys

class Command(BaseCommand):
    help = 'Imports a CSV guestlist to the RSVP table'

    def handle(self, *args, **options):
        '''Import CSV from STDIN with following fields:

        Key:    comma-separated last names that are used, along with address, to
                group RSVP people into a single RSVP
        First:  First name
        Last:   Last name
        Address:Full address, including City, State/Country, Zip

        The CSV should be comma-separated with " as the quote char, and should
        not include a header column.

        Note that this is designed to load all RSVPs from a blank slate - it
        makes no attempt to deduplicate or associate new RSVPPersons with
        existing RSVPs.

        '''
        reader = csv.reader(sys.stdin, delimiter=',')
        seen_rsvps = {}
        # TODO support a header that defines these dynamically
        field_index = {
            'Key': 0,
            'First': 1,
            'Last': 2,
            'Address': 3,
        }
        for row in reader:
            key = row[field_index['Key']]
            if key not in seen_rsvps:
                rsvp = RSVP(
                    last_names=key,
                    invite_address=row[field_index['Address']],
                )
                rsvp.save()
                seen_rsvps[key] = rsvp

            rsvp_person = RSVPPerson(
                rsvp=seen_rsvps[key],
                name='{} {}'.format(
                    row[field_index['First']],
                    row[field_index['Last']],
                ),
            )
            rsvp_person.save()
