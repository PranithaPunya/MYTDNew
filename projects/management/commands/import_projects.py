import pandas as pd
from django.core.management.base import BaseCommand
from projects.models import Project


class Command(BaseCommand):
    help = "Import Excel data into Project model"

    def add_arguments(self, parser):
        parser.add_argument("excel_path", type=str, help="Path to the Excel file")

    def handle(self, *args, **kwargs):
        excel_path = kwargs["excel_path"]
        df = pd.read_excel(excel_path, header=1)  # Start from 2nd row

        created_count = 0
        skipped_count = 0

        for index, row in df.iterrows():
            mydc_ref = self.safe_get_int(row, "MyDC Ref")

            if not mydc_ref:
                self.stdout.write(self.style.WARNING(f"Skipping row {index} - Missing MyDC Ref"))
                skipped_count += 1
                continue

            # Check for duplicate before creating
            if Project.objects.filter(mydc_ref=mydc_ref).exists():
                self.stdout.write(self.style.WARNING(f"Skipping row {index} - Duplicate MyDC Ref: {mydc_ref}"))
                skipped_count += 1
                continue

            project = Project(
                month=self.safe_get_str(row, "Month"),
                mydc_ref=mydc_ref,
                otp=self.safe_get_str(row, "OTP"),
                project=self.safe_get_str(row, "Project"),
                customer=self.safe_get_str(row, "Customer"),
                business_unit=self.safe_get_str(row, "Business unit"),
                global_iqp=self.safe_get_str(row, "Global IQP"),
                bo_pm=self.safe_get_str(row, "BO-PM"),
                bo_pl2=self.safe_get_str(row, "BO-PL2"),
                bo_acqp_maturity=self.safe_get_str(row, "BO ACQP Maturity"),
                bo_acqp_assessment_date=self.safe_get_date(row, "BO ACQP Assessment Date"),
                planned_deliverables=self.safe_get_int(row, "No. of Planned deliverables"),
                otd=self.safe_get_int(row, "No. of on  time deliverables"),
                otd_target=self.safe_get_float(row, "OTD Target"),
                actual_otd_percent=self.safe_get_float(row, "Actual OTD %"),
                right_first_time=self.safe_get_int(row, "No.Of Right First Time Delivered"),
                rft_target=self.safe_get_float(row, "RFT Target"),
                actual_rft_percent=self.safe_get_float(row, "Actual RFT %"),
                skill_compliance=self.safe_get_float(row, "Skill Compliance (Average team's skill level)"),
                csat_level=self.safe_get_int(row, "CSAT level\n(1 to 4)"),
                csat_date=self.safe_get_date(row, "CSAT Date"),
                csat_service_mgmt=self.safe_get_int(row, "CSAT Level\nALTEN service management"),
                csat_quality=self.safe_get_int(row, "CSAT Level\nQuality of deliveries"),
                csat_autonomy=self.safe_get_int(row, "CSAT Level\nAutonomy"),
                csat_communication=self.safe_get_int(row, "CSAT Level\nCommunication"),
                csat_flexibility=self.safe_get_int(row, "CSAT Level\nFlexibility / Reactivity"),
                csat_proactivity=self.safe_get_int(row, "CSAT Level\nPro-Activity"),
                fte_count=self.safe_get_float(row, "Number of FTE"),
                attrition=self.safe_get_int(row, "Project Attrition"),
                replaced_fte=self.safe_get_int(row, "Number of replaced FTE"),
                real_capacity_hours=self.safe_get_float(row, "Real Capacity excluding leaves (h)"),
                time_sold_hours=self.safe_get_float(row, "Time sell to customer (h)"),
                turnover_engaged=self.safe_get_float(row, "Turnover engage by Customer"),
                cumulative_turnover_engaged=self.safe_get_float(row, "Cumulative Turnover engage by Customer"),
                po_received=self.safe_get_float(row, "PO Received"),
                cumulative_po_received=self.safe_get_float(row, "Cumulative PO Received"),
                current_dan=self.safe_get_float(row, "Current Month DAN"),
                cumulative_dan=self.safe_get_float(row, "Cumulative DAN"),
                std_target_margin=self.safe_get_float(row, "STD target margin"),
                std_forecasted_margin=self.safe_get_float(row, "STD margin forecasted"),
                remark=self.safe_get_str(row, "Remark"),
            )

            project.save()
            created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import completed. {created_count} created, {skipped_count} skipped (duplicates/missing refs)."
        ))

    # Helper functions
    def safe_get_str(self, row, column_name):
        value = row.get(column_name)
        return "" if pd.isna(value) else str(value).strip()

    def safe_get_int(self, row, column_name):
        value = row.get(column_name)
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def safe_get_float(self, row, column_name):
        value = row.get(column_name)
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def safe_get_date(self, row, column_name):
        value = row.get(column_name)
        try:
            return pd.to_datetime(value).date()
        except (ValueError, TypeError):
            return None