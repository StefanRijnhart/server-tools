# Copyright 2025 Opener B.V. <https://opener.amsterdam>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged("-at_install", "post_install")
class TestDatabaseSize(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_model = cls.env["ir.model"].search([("model", "=", "res.partner")])
        cls.today = fields.Date.context_today(cls.env.user)
        # Remove any data
        cls.env.cr.execute("delete from ir_model_size")

    def test_database_size(self):
        """Size table is populated and reports can be generated"""
        # Remove any data
        self.env.cr.execute("delete from ir_model_size")
        with self.assertRaisesRegex(UserError, "not.*any data"):
            self.env["ir.model.size.report"].search([])

        self.env.ref(
            "database_size.ir_cron_ir_model_size_measure"
        ).ir_actions_server_id.run()

        # Backdate the data set
        self.env.cr.execute(
            """
            update ir_model_size
            set measurement_date = measurement_date - interval '10 days'
            """
        )
        self.env["ir.model.size"].invalidate_model(["measurement_date"])

        # Generate a new set
        self.env.ref(
            "database_size.ir_cron_ir_model_size_measure"
        ).ir_actions_server_id.run()

        # Retrieve the comparison
        report = self.env["ir.model.size.report"].search(
            [
                ("model_id", "=", self.partner_model.id),
                ("measurement_date", "=", self.today),
                ("historical_measurement_date", "=", self.today - timedelta(days=10)),
            ]
        )
        self.assertTrue(report)

        # Run the action to open the details
        action = report.action_open_model_sizes()
        partner_sizes = self.env["ir.model.size"].search(
            [("model_id", "=", self.partner_model.id)]
        )
        self.assertEqual(len(partner_sizes), 2)
        self.assertEqual(
            self.env[action["res_model"]].search(action["domain"]),
            partner_sizes,
        )

        # Test default dates
        report2 = self.env["ir.model.size.report"].search(
            [("model_id", "=", self.partner_model.id)]
        )
        # Default measurement date is the most recent date
        self.assertEqual(report2.measurement_date, self.today)
        # Default historical measurement date is the most recent date
        # within the last month
        self.assertEqual(
            report2.historical_measurement_date,
            self.today - timedelta(days=10),
        )

        # Test missing data for date
        with self.assertRaisesRegex(UserError, "no data from"):
            self.env["ir.model.size.report"].search(
                [
                    ("model_id", "=", self.partner_model.id),
                    (
                        "historical_measurement_date",
                        "=",
                        self.today - timedelta(days=11),
                    ),
                ]
            )

    def test_database_size_report_diff(self):
        """Size report returns the expected values"""
        with self.assertRaisesRegex(UserError, "not.*any data"):
            self.env["ir.model.size.report"].search([])
        self.env.ref(
            "database_size.ir_cron_ir_model_size_measure"
        ).ir_actions_server_id.run()
        self.env["ir.model.size"].flush_model()

        # Forge some data for the partner model
        self.env.cr.execute(
            """
            update ir_model_size set
            total_database_size = coalesce(total_database_size, 0) + 10,
            total_model_size = coalesce(total_model_size, 0) + 5
            where model_id = %(model_id)s and measurement_date = %(self.today)s
            returning id;
            """,
            {"model_id": self.partner_model.id, "self.today": self.today},
        )

        # Backdate the data set
        self.env.cr.execute(
            """
            update ir_model_size
            set measurement_date = measurement_date - interval '10 days'
            """
        )

        # Generate a new set
        self.env.ref(
            "database_size.ir_cron_ir_model_size_measure"
        ).ir_actions_server_id.run()
        self.env["ir.model.size"].flush_model()

        # Forge data for the partner model in the latest data set
        self.env.cr.execute(
            """
            update ir_model_size set
            total_database_size = coalesce(total_database_size, 0) + 15,
            total_model_size = coalesce(total_model_size, 0) + 11
            where model_id = %(model_id)s and measurement_date = %(self.today)s
            returning id;
            """,
            {"model_id": self.partner_model.id, "self.today": self.today},
        )

        # Retrieve the comparison
        report = self.env["ir.model.size.report"].search(
            [
                ("model_id", "=", self.partner_model.id),
                ("measurement_date", "=", self.today),
                ("historical_measurement_date", "=", self.today - timedelta(days=10)),
            ]
        )

        # Size growth is indicated as expected
        self.assertEqual(report.diff_total_database_size, 5)
        self.assertEqual(report.diff_total_model_size, 6)
