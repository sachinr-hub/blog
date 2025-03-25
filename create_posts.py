import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
django.setup()

from app.models import User, BlogPost, Category

try:
    # Get users
    maya = User.objects.get(username='maya_writer')
    print("Found user Maya")
    sam = User.objects.get(username='sam_journalist')
    print("Found user Sam")
    zara = User.objects.get(username='zara_editor')
    print("Found user Zara")

    # Get categories
    politics = Category.objects.get(slug='politics')
    science = Category.objects.get(slug='science')
    environment = Category.objects.get(slug='environment')
    print("Found all categories")

    # Maya's post
    try:
        maya_post = BlogPost.objects.create(
            title='Global Democracy Index Shows Concerning Trends in 2024',
            content='''The latest Global Democracy Index report, released this week, reveals troubling shifts in democratic governance worldwide. According to the comprehensive analysis of 165 countries, overall democratic health has declined for the fourth consecutive year, with significant deterioration observed in previously stable regions.

Most concerning is the rise of what researchers term "managed democracies" – systems that maintain democratic appearances through elections but undermine essential democratic functions through media restrictions, judicial interference, and limitations on civil society organizations. These hybrid regimes now account for nearly 35% of governments worldwide, up from 28% just five years ago.

Bright spots do exist, however. Several nations have strengthened democratic institutions through constitutional reforms, increased transparency measures, and improved electoral processes. Notably, civic engagement among younger generations has surged, with digital platforms enabling new forms of participation and accountability.

Experts emphasize that democracy's resilience depends on active citizenship and institutional safeguards against power concentration. "Democracy isn't just about voting," notes lead researcher Dr. Elena Mendoza. "It requires independent courts, press freedom, respect for minority rights, and spaces for peaceful dissent – elements increasingly under pressure globally."

As international attention focuses on multiple upcoming elections in pivotal nations this year, the report serves as both warning and call to action for citizens and leaders committed to democratic principles.''',
            author=maya
        )
        maya_post.categories.add(politics)
        print("Maya's post created successfully")
    except Exception as e:
        print(f"Error creating Maya's post: {e}")

    # Sam's post
    try:
        sam_post = BlogPost.objects.create(
            title='Breakthrough in Quantum Computing: Practical Applications Now Within Reach',
            content='''Scientists at the Quantum Research Institute have achieved what many considered impossible just a year ago: a stable quantum computer that operates at room temperature. This breakthrough, published yesterday in the journal Nature Quantum, eliminates one of the biggest obstacles to practical quantum computing—the need for extreme cooling systems.

The team, led by Dr. Hiroshi Nakamura, demonstrated a quantum processor with 128 qubits that maintained quantum coherence for over 15 minutes at standard room conditions. Previous systems required temperatures approaching absolute zero (-273°C) and could only maintain coherence for milliseconds.

"This changes everything about how we approach quantum computing," explains Dr. Nakamura. "We've moved from specialized laboratory equipment to potentially desktop-accessible technology."

The implications are vast. Quantum computers excel at solving complex problems that would take traditional computers millennia to calculate. Fields likely to see immediate benefits include drug discovery, where quantum computers can simulate molecular interactions with unprecedented accuracy, and cryptography, where they could develop new security protocols resistant to quantum-based attacks.

Financial markets are already responding to the news, with significant jumps in stock prices for companies positioned to commercialize quantum technologies. Industry analysts predict the first commercial room-temperature quantum computers could reach specialized markets within three years, with more widespread applications following shortly thereafter.

While challenges remain in scaling the technology and developing quantum-specific software, this breakthrough has undoubtedly accelerated the quantum computing timeline by at least a decade.''',
            author=sam
        )
        sam_post.categories.add(science)
        print("Sam's post created successfully")
    except Exception as e:
        print(f"Error creating Sam's post: {e}")

    # Zara's post
    try:
        zara_post = BlogPost.objects.create(
            title='Ocean Plastic Cleanup Efforts Show First Signs of Ecosystem Recovery',
            content='''For the first time since large-scale ocean cleanup initiatives began a decade ago, marine biologists are reporting measurable recovery in previously devastated marine ecosystems. The latest data from the International Ocean Conservation Coalition shows a 23% reduction in floating plastic debris in targeted cleanup zones, with corresponding increases in marine biodiversity.

The most dramatic improvements have been observed around the Ocean Cleanup Array in the North Pacific Gyre, where plastic concentration has decreased by nearly one-third since deployment. Marine biologists monitoring the area have documented the return of several species that had abandoned the region, including various plankton species that form the critical base of the marine food web.

"We're seeing nature's remarkable resilience in action," explains marine ecologist Dr. Anika Patel. "Remove the stressors, and ecosystems begin to heal themselves—sometimes more quickly than we anticipated."

These positive results come from a combination of improved cleanup technologies and unprecedented international cooperation. The United Nations Ocean Treaty, ratified by 137 countries last year, has established coordinated cleanup zones and stricter regulations on plastic production and disposal.

Equally important has been the dramatic shift in consumer behavior and corporate practices. Single-use plastic consumption has fallen by 47% globally over five years, driven by both regulation and changing consumer preferences.

Despite these encouraging signs, scientists emphasize that ocean plastic pollution remains an urgent crisis. Microplastics continue to permeate every level of marine ecosystems, and many deep-ocean environments show little improvement so far.

"We're just beginning to reverse decades of damage," cautions Dr. Patel. "But for the first time, we have evidence that our collective efforts are making a real difference."''',
            author=zara
        )
        zara_post.categories.add(environment)
        print("Zara's post created successfully")
    except Exception as e:
        print(f"Error creating Zara's post: {e}")

    print("Script completed successfully")
except Exception as e:
    print(f"Error in script: {e}", file=sys.stderr) 