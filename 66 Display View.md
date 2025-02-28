<link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet"/>

# Generic Display View

The two following generic class-based views are designed to display data. On many projects they are typically the most commonly used views.

## DetailView

```python
class django.views.generic.detail.DetailView
```

While this view is executing, self.object will contain the object that the view is operating upon.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.detail.SingleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.detail.BaseDetailView
django.views.generic.detail.SingleObjectMixin
django.views.generic.base.View
```

Method Flowchart

```text
setup()
dispatch()
http_method_not_allowed()
get_template_names()
get_slug_field()
get_queryset()
get_object()
get_context_object_name()
get_context_data()
get()
render_to_response()
```

Example myapp/views.py:

```python
from django.utils import timezone
from django.views.generic.detail import DetailView

from articles.models import Article

class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
```

Example myapp/urls.py:

```python
from django.urls import path

from article.views import ArticleDetailView

urlpatterns = [
    path("<slug:slug>/", ArticleDetailView.as_view(), name="article-detail"),
]
```

Example myapp/article_detail.html:

```html
<h1>{{ object.headline }}</h1>
<p>{{ object.content }}</p>
<p>Reporter: {{ object.reporter }}</p>
<p>Published: {{ object.pub_date|date }}</p>
<p>Date: {{ now|date }}</p>
```

```python
class django.views.generic.detail.BaseDetailView
```

A base view for displaying a single object. It is not intended to be used directly, but rather as a parent class of the django.views.generic.detail.DetailView or other views representing details of a single object.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.detail.SingleObjectMixin
django.views.generic.base.View
```

### 1. Methods

```python
get(request, *args, **kwargs)
```

Adds object to the context.

## ListView

```python
class django.views.generic.list.ListView
```

A page representing a list of objects.

While this view is executing, self.object_list will contain the list of objects (usually, but not necessarily a queryset) that the view is operating upon.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.list.MultipleObjectTemplateResponseMixin
django.views.generic.base.TemplateResponseMixin
django.views.generic.list.BaseListView
django.views.generic.list.MultipleObjectMixin
django.views.generic.base.View
```

Method Flowchart

```text
setup()
dispatch()
http_method_not_allowed()
get_template_names()
get_queryset()
get_context_object_name()
get_context_data()
get()
render_to_response()
```

Example views.py:

```python
from django.utils import timezone
from django.views.generic.list import ListView

from articles.models import Article

class ArticleListView(ListView):
    model = Article
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context
```

Example myapp/urls.py:

```python
from django.urls import path

from article.views import ArticleListView

urlpatterns = [
    path("", ArticleListView.as_view(), name="article-list"),
]
```

Example myapp/article_list.html:

```html
<h1>Articles</h1>
<ul>
{% for article in object_list %}
    <li>{{ article.pub_date|date }} - {{ article.headline }}</li>
{% empty %}
    <li>No articles yet.</li>
{% endfor %}
</ul>
```

If you’re using pagination, you can adapt the example template from the pagination docs.

```python
class django.views.generic.list.BaseListView
```

A base view for displaying a list of objects. It is not intended to be used directly, but rather as a parent class of the django.views.generic.list.ListView or other views representing lists of objects.

Ancestors (MRO)

This view inherits methods and attributes from the following views:

```python
django.views.generic.list.MultipleObjectMixin
django.views.generic.base.View
```

Methods

```python
get(request, *args, **kwargs)
```

Adds object_list to the context. If allow_empty is True then display an empty list. If allow_empty is False then raise a 404 error.
