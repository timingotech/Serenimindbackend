from django.core.management.base import BaseCommand

from api.models import ActivityMovie, ActivityGame, ActivityExercise, ActivitySound


class Command(BaseCommand):
    help = "Seed curated Activity Lounge content (movies, games, exercises, sounds). Safe to run multiple times."

    def handle(self, *args, **options):
        self.stdout.write("Seeding Activity Lounge content...")

        self._seed_movies()
        self._seed_games()
        self._seed_exercises()
        self._seed_sounds()

        self.stdout.write(self.style.SUCCESS("Activity Lounge content seeded (idempotent)."))

    def _seed_movies(self):
        data = [
            {
                "title": "Inside Out",
                "description": "Animated film exploring emotions and mental wellbeing in a fun, heartfelt way.",
                "image_url": "https://image.tmdb.org/t/p/w500/inside-out-poster.jpg",
                "external_url": "https://www.disneyplus.com/movies/inside-out/5Kx7",
                "moods": "anxious,overwhelmed,curious",
            },
            {
                "title": "The Pursuit of Happyness",
                "description": "Inspiring true story about resilience, hope, and never giving up.",
                "image_url": "https://image.tmdb.org/t/p/w500/pursuit-of-happyness.jpg",
                "external_url": "https://www.netflix.com/",
                "moods": "low,motivated,hopeful",
            },
            {
                "title": "Soul",
                "description": "A gentle reminder to slow down and rediscover meaning in everyday life.",
                "image_url": "https://image.tmdb.org/t/p/w500/soul-poster.jpg",
                "external_url": "https://www.disneyplus.com/movies/soul/2MmV",
                "moods": "reflective,stressed,curious",
            },
        ]

        for item in data:
            obj, created = ActivityMovie.objects.get_or_create(
                title=item["title"], defaults=item
            )
            if created:
                self.stdout.write(f"  + Movie: {obj.title}")

    def _seed_games(self):
        data = [
            {
                "title": "Calm Breathing Bubble",
                "description": "Simple breathing game: follow the bubble as it expands and contracts.",
                "image_url": "https://example.com/images/breathing-bubble.png",
                "play_url": "https://www.calm.com/breathe",
                "moods": "anxious,stressed",
            },
            {
                "title": "Color Match Focus",
                "description": "Light, low-pressure color matching game to gently refocus your mind.",
                "image_url": "https://example.com/images/color-match.png",
                "play_url": "https://www.coolmathgames.com/",
                "moods": "distracted,overwhelmed",
            },
            {
                "title": "Gratitude Quiz",
                "description": "Short reflective quiz that nudges you to notice small positives.",
                "image_url": "https://example.com/images/gratitude-quiz.png",
                "play_url": "https://www.verywellmind.com/",
                "moods": "low,reflective",
            },
        ]

        for item in data:
            obj, created = ActivityGame.objects.get_or_create(
                title=item["title"], defaults=item
            )
            if created:
                self.stdout.write(f"  + Game: {obj.title}")

    def _seed_exercises(self):
        data = [
            {
                "name": "Box Breathing (4-4-4-4)",
                "exercise_type": "breathing",
                "reason": "A simple structured breathing pattern that calms the nervous system.",
                "gif_url": "https://example.com/gifs/box-breathing.gif",
                "moods": "anxious,panicky,stressed",
            },
            {
                "name": "5-4-3-2-1 Grounding",
                "exercise_type": "grounding",
                "reason": "Helps bring attention back to the present using the five senses.",
                "gif_url": "https://example.com/gifs/grounding-54321.gif",
                "moods": "overwhelmed,anxious",
            },
            {
                "name": "Gentle Neck & Shoulder Stretch",
                "exercise_type": "stretching",
                "reason": "Releases tension that often builds up with stress and screen time.",
                "gif_url": "https://example.com/gifs/neck-shoulder-stretch.gif",
                "moods": "stressed,tired",
            },
        ]

        for item in data:
            obj, created = ActivityExercise.objects.get_or_create(
                name=item["name"], defaults=item
            )
            if created:
                self.stdout.write(f"  + Exercise: {obj.name}")

    def _seed_sounds(self):
        data = [
            {
                "name": "Rain on Window",
                "category": "ambient",
                "duration": "20:00",
                "audio_url": "https://example.com/audio/rain-on-window.mp3",
                "image_url": "https://example.com/images/rain-on-window.jpg",
                "moods": "anxious,restless",
            },
            {
                "name": "Calm Ocean Waves",
                "category": "ambient",
                "duration": "30:00",
                "audio_url": "https://example.com/audio/ocean-waves.mp3",
                "image_url": "https://example.com/images/ocean-waves.jpg",
                "moods": "stressed,can\'t-sleep",
            },
            {
                "name": "Lo-fi Focus Beats",
                "category": "music",
                "duration": "45:00",
                "audio_url": "https://example.com/audio/lofi-focus.mp3",
                "image_url": "https://example.com/images/lofi-focus.jpg",
                "moods": "distracted,studying,working",
            },
        ]

        for item in data:
            obj, created = ActivitySound.objects.get_or_create(
                name=item["name"], defaults=item
            )
            if created:
                self.stdout.write(f"  + Sound: {obj.name}")
