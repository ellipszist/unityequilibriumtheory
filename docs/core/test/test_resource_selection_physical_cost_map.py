import unittest

from docs.core.resource_selection_physical_cost_map import (
    PhysicalCostMapRecord,
    PhysicalCostMapValidationError,
    map_normalized_work_to_si,
)


class PhysicalCostMapTests(unittest.TestCase):
    def test_open_map_cannot_convert_to_si(self):
        record = PhysicalCostMapRecord(
            map_id="open-map",
            material_or_system="unspecified",
        )
        with self.assertRaises(PhysicalCostMapValidationError):
            map_normalized_work_to_si(0.25, 0.1, record)

    def test_fit_origin_is_rejected(self):
        record = PhysicalCostMapRecord(
            map_id="fit-map",
            material_or_system="test-material",
            behavior_energy_scale_j=2.0,
            maintenance_energy_scale_j=3.0,
            bath_temperature_k=300.0,
            source_locator="fit://target-data",
            source_hash="not-a-source-hash",
            uncertainty_record="missing-independent-uncertainty",
            measurement_operator_id="heat",
            parameter_origin="fit",
        )
        with self.assertRaises(PhysicalCostMapValidationError):
            record.validate_contract()

    def test_ready_test_fixture_maps_work_and_entropy(self):
        record = PhysicalCostMapRecord(
            map_id="fixture-map",
            material_or_system="test-material",
            behavior_energy_scale_j=2.0,
            maintenance_energy_scale_j=3.0,
            bath_temperature_k=300.0,
            source_locator="synthetic://physical-cost-contract",
            source_hash="fixture-hash",
            uncertainty_record="fixture-only",
            measurement_operator_id="integrated_heat_fixture",
            parameter_origin="test_fixture",
            status="TEST_ONLY",
        )
        result = map_normalized_work_to_si(0.25, 0.1, record)
        self.assertAlmostEqual(result.heat_j, 0.8, places=12)
        self.assertAlmostEqual(result.entropy_j_per_k, 0.8 / 300.0, places=12)
        self.assertEqual(result.measurement_operator_id, "integrated_heat_fixture")

    def test_negative_normalized_work_is_rejected(self):
        record = PhysicalCostMapRecord(
            map_id="fixture-map",
            material_or_system="test-material",
            behavior_energy_scale_j=2.0,
            maintenance_energy_scale_j=3.0,
            bath_temperature_k=300.0,
            source_locator="synthetic://physical-cost-contract",
            source_hash="fixture-hash",
            uncertainty_record="fixture-only",
            measurement_operator_id="integrated_heat_fixture",
            parameter_origin="test_fixture",
        )
        with self.assertRaises(PhysicalCostMapValidationError):
            map_normalized_work_to_si(-0.1, 0.1, record)

    def test_wrong_unit_lane_is_rejected(self):
        record = PhysicalCostMapRecord(
            map_id="normalized-map",
            material_or_system="test-material",
            unit_lane="normalized",
        )
        with self.assertRaises(PhysicalCostMapValidationError):
            record.validate_contract()


if __name__ == "__main__":
    unittest.main()
