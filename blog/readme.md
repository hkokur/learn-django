# Summary
In this section, my purpose have been list posts page by page like any blog. i have listed post with 2 approach, function-based view and generic-class-based view.

# Function-Based View
with 3 basic step, any action that desired could been perform
    + get objects from model and filter what you want
    + split querylist by paginator 
    + get page from paginator object

Acording to these steps, i have obtained posts that published out of all posts.
i have split them by number i have desired by paginator
i have used .get_page function of paginator object to get exact page requested
and i have returned page requested

# Generic-class-based View
i have used ListView. i configure that pre-configure class with model, paginate_by, queryset etc.
