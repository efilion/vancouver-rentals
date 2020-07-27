from craigslist import CraigslistHousing

postings = CraigslistHousing(site='vancouver', area='van', category='apa').get_results(geotagged=True, limit=20)

for listing in postings:
    print(listing)