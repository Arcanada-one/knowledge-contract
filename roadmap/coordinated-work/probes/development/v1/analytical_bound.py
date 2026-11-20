"""Independent conservation/capacity bound; never imports the simulator."""
from fractions import Fraction


def cut_bounds(case):
    """For zero initial inventory and no scrap: cumulative shipments <= each cut.

    Every shipped good unit crossed all three processing stages. Its work content
    uses work_units_per_good_unit of that stage's processing capacity. Summing
    flows over T periods, nonnegative final inventories cannot create output.
    Availability and work content are fixed deterministic scalars in this probe.
    """
    T = Fraction(case['horizon_periods'])
    cuts = {'material': T * Fraction(str(case['supply_per_period'])),
            'customer_acceptance': T * Fraction(str(case['demand_per_period']))}
    for index, stage in enumerate(case['stages'], 1):
        total_work = T * Fraction(str(stage['nominal_capacity_per_period'])) * Fraction(str(stage['availability_fraction']))
        cuts[f'stage_{index}_work'] = total_work / Fraction(str(stage['work_units_per_good_unit']))
    return cuts


def shipment_upper_bound(case):
    return min(cut_bounds(case).values())
