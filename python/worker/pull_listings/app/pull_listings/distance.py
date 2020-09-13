class Distance():

    def __init__(self, distance_matrix_provider):
        self.distMatrix = distance_matrix_provider

    def commute_time(self, origin, destination):
        travel_distance = self.distMatrix.distance_matrix(\
            origin=origin,
            destination=destination,
            mode="transit",
            transit_routing_preference="fewer_transfers")
        unpack_travel_distance = travel_distance['rows'][0]['elements'][0]
        duration_value = unpack_travel_distance['duration']['value']
        duration_text = unpack_travel_distance['duration']['text']
        return duration_value, duration_text
