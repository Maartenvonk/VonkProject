class Headers:
    #namen van de headers
    flightNr = "Flight-Flight"
    route = "Flight-Route"
    destination = "Flight-Destination"
    country = "Flight-Country"
    carrier = "Carrier"
    firmnessCode = "Firmness-Code"
    firmnessB2BB2C = "Firmness-B2B vs B2C"
    tourOperator = "Tour Operator-1"
    headerDate = "Date"
    month = "Month"
    year = "Year"
    yoy = "Year over Year"
    snapshot = "Snapshots"
    hub = "Hub"
    flightType = "Flight type"
    direction = "Direction"
    businessRule = "Flight type"
    capacity = "Aircraft Capacity"
    allocatedSeats = "Allocated Seats"
    ancillaryRev = "Ancillary Revenue"
    pax = "# Pax"
    seatsSold = "Seats Sold"
    ticketRev = "Ticket Revenue"
    totalRev = "Total Revenue"
    day_of_week = "Day of week"
    load_factor = "Commercial %"
    lid_percentage = "Lid %"
    pax_percentage = "Pax %"
    day_before_departure = "Days before departure"
    estimated_var_costs = "Estimated variable cost"
    legs = "# Legs"
    average_lowest_available_fare = "Average Lowest Available Fare"
    fare_grid_basic = "Fare Grid Basic"

    #namen van headers yielddata
    ticketYield = "Ticket Yield"
    totalYield = "Total Yield"

    #namen van de tour-op
    B2C = "B2C"
    guaranteed = "Guaranteed"
    nonGuaranteed = "Non guaranteed"
    empty = ""

    #headers boeking curves
    BC_lfRoute = "Group"
    BC_mediumLF = "Medium LF"
    BC_br = "BR"
    BC_dbd = "DBD"
    Y_class = "Y"
    Z_class = "Z"
    J_class = "J"
    S_class = "S"
    D_class = "D"
    B_class = "B"
    I_class = "I"
    M_class = "M"
    H_class = "H"
    Q_class = "Q"
    V_class = "V"
    K_class = "K"
    L_class = "L"
    R_class = "R"
    T_class = "T"
    G_class = "G"
    N_class = "N"
    A_class = "A"

    #c1 kosten
    c1costs = "Forecast Cost C1 per flight"

    #yield koppeltabel
    yieldRoute = "Yield-Route"
    yieldFactor = "Yield-Factor"
    previousMonth = "Yield Month"
    zakelijk = "Zakelijk"

    #c1 koppeltabel
    financialRoute = "Financial-Route"
    commercialRoute = "Commercial-Route"

    #Charter koppel C1
    costs = "Variable cost adjusted"

    #headers pricing / businessrules
    fareclass = "Fare class-Fare Class"
    faregroup = "Fare class-Fare Group"
    brroute = "BR Route"
    br = "Business Rule"
    nrbusinessrules = "# Business Rules"
    flight_flight = "Flight-Flight"
    flight_route_flight_nr = "Flight-Route with fltnr"
    lac = "Lowest Available Class"
    bl_lowerbound = "Base Load LowB"
    bl_upperbound = "Base Load UppB"
    bl= "Base Load"
    bl_cat0 = "Baseload Cat-0"
    bl_importance = "Baseload Importance"



    #headers QL2
    departure_time_ql2 = "Departure Time"
    flight_carrier_route_ql2 = "Flight-Carrier-Route"
    average_fare_ql2 = "Avg Fare"
    flight_date_ql2 = "Flight day"
    snapshot_ql2 = "Snapshot"

    #headers QL2 boundaries
    HVTOroute_ql2 = "HV/TO route"
    time_boundary_ql2 = "Time boundary"
    lower_boundary_ql2 = "Lower boundary"
    upper_boundary_ql2 = "Upper boundary"


class SftHeaders:
    def __init__(self):
        self.book_month = 'Book month'
        self.ticket_revenue = 'ticket revenue'
        self.flight_flight = 'Flight-Flight'
        self.flight_destination = 'Flight-Destination'
        self.flight_date = 'Flight date-0'
        self.airpas_route = 'Airpas route-Route'
        self.forecast_milestone = 'Milestone'
        self.forecast_version = 'Version-Version'
        self.hub = 'Hub-0'
        self.flight_route = 'Route-Route'
        self.flight_type = 'flight type-0'
        self.direction = 'Direction-Direction'
        self.third_party_revenue = '3rd party revenue'
        self.on_board_revenue = 'On board revevenue'
        self.ancillary_rev_excl_onboard_3rd_party = 'Ancillary revenue (excl On board/3rd party)'
        self.ancillary_rev_excl_onboard_3rd_party_b2b = 'Ancillary revenue (excl On board/3rd party) B2B'
        self.ancillary_rev_excl_onboard_3rd_party_b2c = 'Ancillary revenue (excl On board/3rd party) B2C'
        self.total_ancl_rev = 'Total ancillary revenue'
        self.ask = 'ASK'
        self.flight_cap = 'Capacity'
        self.total_seats_sold = 'Seats sold '
        self.total_seats_sold_b2b = 'Seats sold B2B'
        self.total_seats_sold_b2c = 'Seats sold B2C'
        self.total_ticket_rev = 'Ticket revenue'
        self.total_ticket_rev_b2b = 'Ticket revenue B2B'
        self.total_ticket_rev_b2c = 'Ticket revenue B2C'


class BaseloadSettings:
    # headers boundary settings
    BS_variable = "Variable"
    BS_boundary = "Boundary"
    BS_value = "Value"
    BS_nonhub = "NonHub"
    BS_default = "Default"
    BS_lowlid = "LowLid"
    BS_competitor = "Competitor"
    BS_leisure = "Leisure"
    BS_business = "Business"
    BS_more_early = "More early booking"
    BS_more_late = "More late booking"
    BS_ub_value = "OverwriteUB_Value"
    BS_ub_dbd = "OverwriteUB_DBD"
    BS_lb_value = "OverwriteLB_Value"
    BS_lb_dbd = "OverwriteLB_DBD"
    BS_correct_curve_end = "Final LF"
    BS_pickup_advisor = "Pickup"
    BS_low_load_advisor = "Low Load"