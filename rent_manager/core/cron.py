from django_cron import CronJobBase, Schedule
from .invoice_generator import generate_monthly_invoices

class MonthlyInvoiceCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:01']  # 12:01 AM

    schedule = Schedule(run_at_times=RUN_AT_TIMES, day_of_month='5')
    code = 'core.monthly_invoice_cron'  # unique ID

    def do(self):
        generate_monthly_invoices()