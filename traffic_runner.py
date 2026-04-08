import asyncio
import random
import sys
from collections import defaultdict
from protocol.codec import encode
from protocol import constants as C
from server.persistence import Database

TICK_SECONDS = 2.0
PUBLISH_PROB = 0.65
COMMENT_PROB = 0.35

NEWS_BANK = {
    "Sports": [
        ("Matchday Update", "Team A secured a late win after extra time."),
        ("Training Report", "The squad completed a strong recovery session today."),
        ("League Table", "The standings changed after tonight's fixtures."),
        ("Transfer Watch", "A new player signing is being discussed by management."),
        ("Injury Update", "A key player is expected to return next week."),
        ("Cup Preview", "The next knockout game is expected to be intense."),
        ("Post Match", "Fans praised the team's defensive performance."),
        ("Youth Academy", "A promising young player was promoted to the first team."),
        ("Stadium News", "Maintenance work was completed ahead of the weekend."),
        ("Captain Interview", "The captain said the squad remains focused."),
    ],
    "Entertainment": [
        ("Box Office", "A new release topped the weekend charts."),
        ("Festival News", "The annual arts festival announced its schedule."),
        ("Streaming Update", "A popular series has been renewed for another season."),
        ("Award Season", "Nominees were announced for this year's major awards."),
        ("Concert Tour", "A world tour has added new international dates."),
        ("Film Review", "Critics praised the visuals and soundtrack."),
        ("Celebrity News", "A public appearance drew major media attention."),
        ("TV Special", "A holiday special is scheduled for next month."),
        ("Premiere Night", "The cast attended the official premiere event."),
        ("Behind the Scenes", "Production updates were shared by the studio."),
    ],
    "Health": [
        ("Clinic Update", "A local campaign is promoting preventive checkups."),
        ("Nutrition News", "Experts highlighted the benefits of balanced meals."),
        ("Sleep Study", "Researchers discussed healthy sleep habits."),
        ("Fitness Advice", "Daily walking was recommended as a simple routine."),
        ("Wellness Program", "A workplace wellness initiative was launched."),
        ("Public Health", "Officials encouraged seasonal vaccination awareness."),
        ("Mental Health", "Community resources were expanded this month."),
        ("Hydration Reminder", "Doctors emphasized hydration during warm weather."),
        ("Routine Care", "Regular screenings were recommended for adults."),
        ("Health Education", "A new seminar will focus on healthy habits."),
    ],
    "Science": [
        ("Space Update", "Researchers reported progress on a satellite mission."),
        ("Lab Results", "A recent experiment produced promising data."),
        ("Climate Study", "Scientists published new environmental findings."),
        ("Biology News", "A team shared insights on cellular behavior."),
        ("Physics Brief", "A conference discussed advances in materials science."),
        ("Research Grant", "Funding was awarded to a university project."),
        ("Ocean Study", "Marine researchers documented ecosystem changes."),
        ("Robotics Lab", "A prototype demonstrated improved motion control."),
        ("Astronomy Note", "Observers recorded unusual stellar activity."),
        ("Science Fair", "Students presented innovative research ideas."),
    ],
    "Technology": [
        ("Product Launch", "A company unveiled a new device today."),
        ("Security Update", "A patch addressed several software issues."),
        ("AI News", "A new model was released for public testing."),
        ("Cloud Services", "An infrastructure provider expanded capacity."),
        ("Chip Industry", "A manufacturer announced a production update."),
        ("Mobile Update", "A system update introduced performance improvements."),
        ("Developer Tools", "A new SDK was released for app creators."),
        ("Startup Watch", "A young company introduced a new platform."),
        ("Open Source", "A community project added major features."),
        ("Tech Conference", "Speakers focused on automation and scalability."),
    ],
    "Politics": [
        ("Parliament News", "Debate continued on a major policy proposal."),
        ("Election Update", "Candidates held public campaign events today."),
        ("Policy Brief", "A new plan was introduced for public consultation."),
        ("Diplomatic Visit", "Officials met to discuss bilateral cooperation."),
        ("Committee Report", "A review panel released preliminary findings."),
        ("Budget News", "Spending priorities were presented this morning."),
        ("Local Government", "Council members voted on a transport project."),
        ("Press Conference", "Leaders answered questions on recent decisions."),
        ("Legislation", "A bill advanced to the next stage."),
        ("International Affairs", "Talks resumed between regional delegates."),
    ],
    "Business": [
        ("Market Watch", "Investors reacted to the latest earnings reports."),
        ("Company Update", "A firm announced a restructuring plan."),
        ("Retail News", "Sales trends improved over the last quarter."),
        ("Supply Chain", "Logistics delays were reduced this month."),
        ("Startup Funding", "A new financing round was completed."),
        ("Quarterly Results", "Revenue increased compared to last year."),
        ("Industry News", "Manufacturers reported stable demand."),
        ("Expansion Plan", "A company opened a new regional office."),
        ("Hiring News", "Recruitment activity increased across the sector."),
        ("Trade Report", "Analysts discussed recent export figures."),
    ],
}

COMMENT_BANK = {
    "Sports": [
        "Great result for the team.",
        "That was a strong performance.",
        "Interesting match update.",
        "I did not expect that outcome.",
        "The timing of that win is important.",
        "Looks like momentum is building.",
        "That could change the season.",
        "Very solid news for supporters.",
        "I want to see the next game now.",
        "This should boost confidence.",
    ],
    "Entertainment": [
        "That sounds exciting.",
        "I want to check this out.",
        "Interesting entertainment update.",
        "That will probably attract attention.",
        "Good timing for this release.",
        "This could become very popular.",
        "The audience will like this.",
        "That is a strong promotion move.",
        "I am curious to see the reaction.",
        "This looks promising.",
    ],
    "Health": [
        "That is useful health advice.",
        "Good reminder for daily habits.",
        "This seems important for the public.",
        "Helpful information for everyone.",
        "That is a positive update.",
        "More people should know this.",
        "A very relevant health topic.",
        "This could help many people.",
        "That sounds like a good initiative.",
        "Practical and important advice.",
    ],
    "Science": [
        "Very interesting scientific result.",
        "That sounds like meaningful progress.",
        "I would like to read more about this.",
        "A strong update from the research side.",
        "This could lead to further discoveries.",
        "That is a fascinating result.",
        "Science keeps moving quickly.",
        "This is worth following closely.",
        "Impressive work from the researchers.",
        "That is a valuable finding.",
    ],
    "Technology": [
        "That is an interesting technology update.",
        "This could be useful in practice.",
        "I want to see how this develops.",
        "That sounds like a solid improvement.",
        "Very relevant for current trends.",
        "This may have a wide impact.",
        "That is a strong technical move.",
        "Interesting direction for the industry.",
        "This could be adopted quickly.",
        "A good update for developers.",
    ],
    "Politics": [
        "That will likely spark discussion.",
        "This could influence future decisions.",
        "Interesting political development.",
        "That is worth monitoring closely.",
        "This may affect many people.",
        "The response to this will matter.",
        "That sounds significant.",
        "A notable policy-related update.",
        "This could shape the debate.",
        "An important development to watch.",
    ],
    "Business": [
        "That is an interesting business update.",
        "This may affect the market.",
        "A strong sign for the sector.",
        "That could influence competitors.",
        "This looks important for investors.",
        "Interesting movement in the business side.",
        "That may shape future strategy.",
        "This sounds like a meaningful shift.",
        "A useful update for the industry.",
        "That is worth keeping an eye on.",
    ],
}

latest_received_by_client = {}
rq_counter = 0


def next_rq():
    global rq_counter
    rq_counter += 1
    return str(rq_counter)


def load_clients(db: Database):
    users = db.list_users()
    by_name = {u["name"]: u for u in users}
    subjects_by_name = {}
    for name in by_name:
        subjects_by_name[name] = db.get_subjects(name)
    return by_name, subjects_by_name


class UdpSender(asyncio.DatagramProtocol):
    def connection_made(self, transport):
        self.transport = transport


async def make_sender():
    loop = asyncio.get_running_loop()
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: UdpSender(),
        local_addr=("0.0.0.0", 0),
    )
    return transport


def sanitize(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ").strip()


async def send_publish(transport, server_ip, server_udp_port, client_name, subject, title, text):
    msg = encode(C.PUBLISH, next_rq(), client_name, sanitize(subject), sanitize(title), sanitize(text))
    transport.sendto(msg.encode(), (server_ip, server_udp_port))
    print(f"[BOT] PUBLISH as {client_name}: {subject} | {title}")


async def send_comment(transport, server_ip, server_udp_port, client_name, subject, title, text):
    msg = encode(C.PUBLISH_COMMENT, client_name, sanitize(subject), sanitize(title), sanitize(text))
    transport.sendto(msg.encode(), (server_ip, server_udp_port))
    print(f"[BOT] COMMENT as {client_name}: {subject} | {title} -> {text}")


async def bot_loop(server_ip: str, server_udp_port: int, db_path: str):
    db = Database(db_path)
    transport = await make_sender()

    try:
        while True:
            by_name, subjects_by_name = load_clients(db)

            if not by_name:
                print("[BOT] No registered clients.")
                await asyncio.sleep(TICK_SECONDS)
                continue

            client_names = list(by_name.keys())
            chosen = random.choice(client_names)

            # Decide whether to comment or publish
            can_comment = chosen in latest_received_by_client
            do_comment = can_comment and random.random() < COMMENT_PROB

            if do_comment:
                latest = latest_received_by_client[chosen]
                subject = latest["subject"]
                title = latest["title"]
                comment_text = random.choice(COMMENT_BANK.get(subject, COMMENT_BANK["Technology"]))
                await send_comment(
                    transport,
                    server_ip,
                    server_udp_port,
                    chosen,
                    subject,
                    title,
                    comment_text,
                )
            else:
                subjects = subjects_by_name.get(chosen, [])
                if not subjects:
                    print(f"[BOT] {chosen} has no subjects, skipping.")
                    await asyncio.sleep(TICK_SECONDS)
                    continue

                subject = random.choice(subjects)
                title, body = random.choice(NEWS_BANK.get(subject, NEWS_BANK["Technology"]))

                await send_publish(
                    transport,
                    server_ip,
                    server_udp_port,
                    chosen,
                    subject,
                    title,
                    body,
                )

                # Approximate “received latest message” for all subscribed clients.
                # Since the server distributes by subject, any registered user with that
                # subject would be a receiver candidate.
                for other_name, other_subjects in subjects_by_name.items():
                    if subject in other_subjects:
                        latest_received_by_client[other_name] = {
                            "publisher": chosen,
                            "subject": subject,
                            "title": title,
                            "text": body,
                        }

            await asyncio.sleep(TICK_SECONDS)

    finally:
        transport.close()


if __name__ == "__main__":
    # Usage:
    # python traffic_runner.py 192.168.0.58 20000 serverA.db
    server_ip = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    server_udp_port = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
    db_path = sys.argv[3] if len(sys.argv) > 3 else "serverA.db"

    asyncio.run(bot_loop(server_ip, server_udp_port, db_path))