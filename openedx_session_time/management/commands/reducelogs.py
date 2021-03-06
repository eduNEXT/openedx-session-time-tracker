"""TODO"""

from datetime import datetime, timedelta
from django.core.management.base import BaseCommand

from student.models import CourseEnrollment
from track.models import TrackingLog

from openedx_session_time.models import SessionLog


class Command(BaseCommand):
    """
        Management Command reducelogs for tracking logs
    """
    help = 'Reduces tracking logs into sessions logs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--from_date',
            type=lambda d: datetime.strptime(d, '%Y%m%d'),
            required=False,
            default=datetime.utcnow() - timedelta(days=1),
        )
        parser.add_argument(
            '--to_date',
            type=lambda d: datetime.strptime(d, '%Y%m%d'),
            required=False,
            default=datetime.utcnow(),
        )

    def handle(self, *args, **options):
        """
            Body of reducelogs command
        """
        from_date = options['from_date']
        to_date = options['to_date']
        valid_logs = self.clean_tracking_logs(
            TrackingLog.objects.filter(time__range=(from_date, to_date)).order_by('time')
        )

        users_with_logs = TrackingLog.objects.order_by().values('username').distinct()
        courses = CourseEnrollment.objects.order_by().values('course_id').distinct()
        reduced_logs = self.reduce_user_logs(users_with_logs, valid_logs, courses)
        self.load_session_logs(reduced_logs)
        self.stdout.write('command finished')

    def clean_tracking_logs(self, queryset):
        """
            Returns a list of valid logs to be reduced
        """
        logs = [log for log in queryset if self.is_valid(log)]

        return logs

    def is_valid(self, log):
        """
            For a log to be valid must have a course_id on event_type field
        """
        is_valid = False
        course_id = None
        try:
            course_id = self.get_course_id(log)
        except Exception:
            self.stdout.write('Discarding invalid Log -- Missing courseid')
        else:
            if course_id:
                is_valid = True

        return is_valid

    def get_user_course_logs(self, logs, course):
        """
            Returns the logs for a course
        """
        user_course_logs = []

        for log in logs:
            course_id = self.get_course_id(log)
            if course.get('course_id') == course_id:
                user_course_logs.append(log)

        return user_course_logs

    def split_logs_by_session(self, user_course_logs, session_duration):
        """
            Method in charge of grouping tracking events
            as session events
        """

        result = []
        acc_list = [user_course_logs[0]]
        for index in range(1, len(user_course_logs)):

            if self.difference(user_course_logs[index - 1], user_course_logs[index]) <= session_duration:
                acc_list.append(user_course_logs[index])
            else:
                result.append(acc_list)
                acc_list = []
                acc_list.append(user_course_logs[index])

        if acc_list:
            result.append(acc_list)

        return filter(lambda x: len(x) >= 2, result)

    @staticmethod
    def difference(log1, log2):
        """
            Computes the time difference between two tracking logs in seconds
        """
        diff = log2.time - log1.time
        return diff.total_seconds()

    def generate_session_logs(self, logslist):
        """
            Returns a session log object for every list of tracking logs
        """
        session_logs = []

        for logs in logslist:
            session_object = {}
            try:
                course_id = self.get_course_id(logs[0])
            except Exception:
                self.stdout.write('Error generating session log -- could not get course_id')
            else:
                session_object = {
                    'username': logs[0].username,
                    'host': logs[0].host,
                    'course_id': course_id,
                    'session_start': logs[0].time,
                    'session_end': logs[-1].time,
                    'session_duration': logs[-1].time - logs[0].time,
                }

                session_logs.append(session_object)

        return session_logs

    def reduce_user_logs(self, users, valid_logs, courses, session_duration=480.0):
        """
            parameter session_duration is in secconds

            This method returns a list with session logs per user
            group by time difference between tracking logs events.

            A session log has this attributes:
            - username
            - courseid
            - session start
            - session end
            - host
            - session duration
        """
        session_logs = []

        for user in users:
            username = user.get('username')
            if username:
                logs_generated_by_user = filter(lambda x: x.username == username, valid_logs)
                for course in courses:
                    user_course_logs = self.get_user_course_logs(logs_generated_by_user, course)
                    if user_course_logs:
                        splitted_course_logs = self.split_logs_by_session(user_course_logs, session_duration)
                        session_logs += self.generate_session_logs(splitted_course_logs)

        return session_logs

    def load_session_logs(self, loglist):
        """
            Creates session log db records
        """
        for session_log in loglist:
            SessionLog.objects.create(
                username=session_log['username'],
                host=session_log['host'],
                courseid=session_log['course_id'],
                start_time=session_log['session_start'],
                end_time=session_log['session_end'],
                session_duration=session_log['session_duration'],
            )
        self.stdout.write('session logs loaded on database')

    @staticmethod
    def get_course_id(log):
        course_id = None

        splitted_event = log.event_type.split("/")
        if 'course-' in splitted_event[2]:
            course_id = splitted_event[2]

        return course_id
