from django.test import TestCase
from .models import Task

class TaskModelTest(TestCase):

    def setUp(self):
        Task.objects.create(title="Test Task", description="Test Description")

    def test_task_content(self):
        task = Task.objects.get(id=1)
        expected_title = f'{task.title}'
        expected_description = f'{task.description}'
        self.assertEqual(expected_title, 'Test Task')
        self.assertEqual(expected_description, 'Test Description')

    def test_task_completed_default(self):
        task = Task.objects.get(id=1)
        self.assertFalse(task.completed)


from django.test import TestCase
from .forms import TaskForm

class TaskFormTest(TestCase):

    def test_valid_form(self):
        form = TaskForm(data={'title': "New Task", 'description': "New Description", 'completed': False})
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = TaskForm(data={'title': "", 'description': "New Description"})
        self.assertFalse(form.is_valid())


from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskViewTest(TestCase):

    def setUp(self):
        Task.objects.create(title="Test Task", description="Test Description")

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo/index.html')

    def test_add_task_view(self):
        response = self.client.post(reverse('add_task'), {
            'title': 'Another Task',
            'description': 'Another Description',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful post
        self.assertEqual(Task.objects.count(), 2)


from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskIntegrationTest(TestCase):

    def test_create_and_retrieve_task(self):
        # Create a new task
        response = self.client.post(reverse('add_task'), {
            'title': 'Integration Task',
            'description': 'Integration Description',
            'completed': False
        })
        self.assertEqual(response.status_code, 302)  # Ensure it redirects after creation

        # Retrieve the task list
        response = self.client.get(reverse('index'))
        self.assertContains(response, 'Integration Task')


from django.test import TestCase
from django.urls import reverse
from .models import Task

class TaskIntegrationTest(TestCase):

    def setUp(self):
        self.task = Task.objects.create(title="Old Task", description="Old Description")

    def test_edit_task(self):
        # Edit the existing task
        response = self.client.post(reverse('edit_task', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated Description',
            'completed': True
        })
        self.assertEqual(response.status_code, 302)

        # Verify the task was updated
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertTrue(self.task.completed)

    def test_delete_task(self):
        # Delete the task
        response = self.client.post(reverse('delete_task', args=[self.task.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.count(), 0)
