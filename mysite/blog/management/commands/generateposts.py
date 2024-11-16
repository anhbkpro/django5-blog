from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post, Comment  # Update with your model imports
from django.utils.text import slugify
from django.utils import timezone
from faker import Faker
import random
from datetime import timedelta
from taggit.models import Tag  # Assuming you're using django-taggit

class Command(BaseCommand):
    help = 'Generate fake blog posts with tags and comments'

    def add_arguments(self, parser):
        parser.add_argument(
            '--number',
            type=int,
            default=100,
            help='Number of posts to create'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Delete existing posts before creating new ones'
        )
        parser.add_argument(
            '--min-comments',
            type=int,
            default=0,
            help='Minimum number of comments per post'
        )
        parser.add_argument(
            '--max-comments',
            type=int,
            default=5,
            help='Maximum number of comments per post'
        )

    def generate_tags(self):
        """Generate a list of common blog tags"""
        common_tags = [
            'Technology', 'Programming', 'Python', 'Django',
            'Web Development', 'Tutorial', 'How-to', 'Guide',
            'Tips', 'Best Practices', 'Software', 'Development',
            'Code', 'Learning', 'Backend', 'Frontend', 'Database',
            'API', 'Security', 'Performance', 'Testing', 'Debug',
            'Framework', 'Library', 'Tools', 'Deployment', 'Cloud',
            'DevOps', 'Architecture', 'Design Patterns'
        ]

        # Create tags if they don't exist
        for tag_name in common_tags:
            Tag.objects.get_or_create(name=tag_name)

        return common_tags

    def generate_rich_content(self, faker):
        """Generate rich content with formatting"""
        paragraphs = []

        # Add a heading
        paragraphs.append(f"# {faker.sentence()}\n")

        # Add introduction
        paragraphs.append(faker.paragraph(nb_sentences=3))

        # Add subheading
        paragraphs.append(f"\n## {faker.sentence()}\n")

        # Add code example
        code_samples = [
            'print("Hello, World!")',
            'def example_function():\n    return True',
            'class ExampleClass:\n    pass',
            'if __name__ == "__main__":\n    main()',
        ]
        paragraphs.append(f"```python\n{random.choice(code_samples)}\n```\n")

        # Add main content with bullet points
        paragraphs.append(faker.paragraph())
        bullet_points = [f"* {faker.sentence()}" for _ in range(random.randint(3, 6))]
        paragraphs.append("\n".join(bullet_points))

        # Add another paragraph
        paragraphs.append(f"\n{faker.paragraph()}\n")

        # Add a quote
        paragraphs.append(f"> {faker.sentence()}\n")

        # Add conclusion
        paragraphs.append(faker.paragraph())

        return "\n\n".join(paragraphs)

    def generate_comments(self, post, faker, min_comments, max_comments):
        """Generate random comments for a post"""
        num_comments = random.randint(min_comments, max_comments)

        for _ in range(num_comments):
            days_after_post = random.randint(0, (timezone.now() - post.publish).days)
            comment_date = post.publish + timedelta(days=days_after_post)

            Comment.objects.create(
                post=post,
                name=faker.name(),
                email=faker.email(),
                body=faker.paragraph(nb_sentences=random.randint(1, 3)),
                created=comment_date,
                active=True
            )

    def handle(self, *args, **kwargs):
        faker = Faker()
        number = kwargs['number']
        min_comments = kwargs['min_comments']
        max_comments = kwargs['max_comments']

        # Delete existing posts if requested
        if kwargs['delete']:
            self.stdout.write('Deleting existing posts...')
            Post.objects.all().delete()
            Comment.objects.all().delete()

        # Generate tags
        common_tags = self.generate_tags()

        # Get or create default author
        default_author, created = User.objects.get_or_create(
            id=1,
            defaults={
                'username': 'admin',
                'email': 'admin@example.com',
                'is_staff': True,
                'is_superuser': True
            }
        )

        if created:
            default_author.set_password('admin123')
            default_author.save()
            self.stdout.write('Created default author (admin)')

        posts_created = 0
        comments_created = 0
        start_time = timezone.now()

        for i in range(number):
            try:
                # Generate title
                title = faker.sentence(nb_words=random.randint(4, 8))
                if len(title) > 200:
                    title = title[:197] + "..."

                # Generate unique slug
                base_slug = slugify(title)
                timestamp = int(timezone.now().timestamp())
                slug = f"{base_slug}-{timestamp}"

                # Generate publish date (distributed over the last year)
                days_ago = random.randint(0, 365)
                publish_date = start_time - timedelta(days=days_ago)

                # Create post with rich content
                post = Post.objects.create(
                    title=title,
                    slug=slug,
                    author=default_author,
                    body=self.generate_rich_content(faker),
                    status='PB',
                    publish=publish_date
                )

                # Add random tags (2-5 tags per post)
                num_tags = random.randint(2, 5)
                selected_tags = random.sample(common_tags, num_tags)
                post.tags.add(*selected_tags)

                # Generate comments for the post
                self.generate_comments(post, faker, min_comments, max_comments)
                current_comments = Comment.objects.filter(post=post).count()
                comments_created += current_comments

                posts_created += 1

                if posts_created % 10 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Created {posts_created} posts with {comments_created} comments...'
                        )
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error creating post: {str(e)}')
                )
                continue

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {posts_created} posts with {comments_created} comments'
            )
        )
