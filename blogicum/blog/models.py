from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse

from config import MAX_LENGTH_NAME, MAX_TITLE_LENGTH

User = get_user_model()


class PostManager(models.Manager):
    """Selects and filters published blog posts"""

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(
                "author",
                "category",
                "location",
            )
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=timezone.now(),
            )
            # .order_by("-pub_date")
        )


class BaseModel(models.Model):
    """Base model for other models."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title[:MAX_TITLE_LENGTH]


class Category(BaseModel):
    """Model representing a category."""

    title = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; '
        'разрешены символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse(
            "blog:category_posts", kwargs={"category_slug": self.slug}
        )


class Location(BaseModel):
    """Model representing a location."""

    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name


class Post(BaseModel):
    """Model representing a post."""

    title = models.CharField(
        max_length=MAX_LENGTH_NAME,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )
    image = models.ImageField(
        "Изображение",
        blank=True,
        upload_to='img/')
    objects = models.Manager()
    post_list = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']
        default_related_name = "posts"

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("blog:post_detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name="Пост",
    )
    text = models.TextField(
        verbose_name="Текст комментария",
    )
    created_at = models.DateTimeField(
        verbose_name="Дата",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ("created_at",)
        default_related_name = "comments"

    def __str__(self):
        return self.text
