def public_view(view_func):
    """Декоратор для пометки публичных страниц"""
    view_func.is_public = True
    return view_func