import os
import discord
from discord.ext import commands
from discord import app_commands
import aiohttp

API_KEY = os.getenv("RIOT_API_KEY")
REGION = "americas"  # (americas, asia, europe, sea)

HEADERS = {
    "X-Riot-Token": API_KEY
}

class Valorant(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def get_summoner(self, region: str, name: str):
        # RiotID#tag separation
        try:
            riot_id, tag = name.split('#')
        except ValueError:
            return None, "Invalid format! Use RiotID#Tag (e.g. azure#bot)"

        url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{riot_id}/{tag}"
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json(), None
            elif resp.status == 404:
                return None, "Player not found."
            else:
                return None, f"Error fetching player info: HTTP {resp.status}"
            
    async def get_rank(self, puuid: str):
        url = f"https://{REGION}.api.riotgames.com/val/ranked/v1/players/{puuid}"
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json(), None
            elif resp.status == 404:
                return None, "Rank data not found."
            else:
                return None, f"Error fetching rank data: HTTP {resp.status}"

    async def get_matchlist(self, puuid: str, count: int = 1):
        url = f"https://{REGION}.api.riotgames.com/val/match/v1/matches/by-puuid/{puuid}/ids?count={count}"
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json(), None
            else:
                return None, f"Error fetching match list: HTTP {resp.status}"

    async def get_match(self, match_id: str):
        url = f"https://{REGION}.api.riotgames.com/val/match/v1/matches/{match_id}"
        async with self.session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.json(), None
            else:
                return None, f"Error fetching match data: HTTP {resp.status}"

    @app_commands.command(name="valorant_recent_match_info", description="Search Valorant recent match info")
    @app_commands.describe(player="RiotID#Tag (ex: azure#bot)")
    async def valorant_recent_match_info(self, interaction: discord.Interaction, player: str):
        
        # Disabled
        await interaction.response.send_message("/valorant_recent_match_info is currently disabled due to API KEY reset")
        return 
        ##############
        
        await interaction.response.defer(thinking=True)

        summoner_info, error = await self.get_summoner("na1", player)
        if error:
            await interaction.followup.send(error)
            return

        puuid = summoner_info['puuid']
        matches, error = await self.get_matchlist(puuid)
        if error or not matches:
            await interaction.followup.send(error or "No matches found.")
            return

        recent_match_id = matches[0]
        match_data, error = await self.get_match(recent_match_id)
        if error:
            await interaction.followup.send(error)
            return

        # simplified
        info = f"**Player:** {player}\n"
        info += f"**Match ID:** {recent_match_id}\n"
        info += f"**Game Mode:** {match_data.get('metadata', {}).get('mode', 'Unknown')}\n"

        participants = match_data.get('players', {}).get('all_players', [])
        player_data = None
        for p in participants:
            if p['puuid'] == puuid:
                player_data = p
                break

        if player_data:
            stats = player_data.get('stats', {})
            info += f"**Agent:** {player_data.get('character', 'Unknown')}\n"
            info += f"**Kills:** {stats.get('kills', 0)}\n"
            info += f"**Deaths:** {stats.get('deaths', 0)}\n"
            info += f"**Assists:** {stats.get('assists', 0)}\n"
            info += f"**Score:** {stats.get('score', 0)}\n"
        else:
            info += "Player stats not found in this match."

        await interaction.followup.send(info)
        
    @app_commands.command(name="valorant_find_player", description="Get Valorant player basic info and rank")
    @app_commands.describe(player="RiotID#Tag (ex: azure#bot)")
    async def valorant_find_player(self, interaction: discord.Interaction, player: str):
        
        # Disabled
        await interaction.response.send_message("/valorant_recent_match_info is currently disabled due to API KEY reset")
        return 
        ##############
        
        await interaction.response.defer(thinking=True)

        summoner_info, error = await self.get_summoner("na1", player)
        if error:
            await interaction.followup.send(error)
            return

        puuid = summoner_info['puuid']
        level = summoner_info.get('account_level', 'Unknown')
        name = summoner_info.get('game_name', 'Unknown')
        tag = summoner_info.get('tag_line', 'Unknown')

        rank_info, error = await self.get_rank(puuid)
        rank = "Unranked"
        ranked_games = 0
        if not error and rank_info:
            current_tier = rank_info.get('currenttierpatched')
            ranked_games = rank_info.get('number_of_games', 0)
            if current_tier:
                rank = current_tier


        match_ids, error = await self.get_matchlist(puuid, count=20)
        normal_games = 0
        if not error and match_ids:
            for match_id in match_ids:
                match_data, err = await self.get_match(match_id)
                if err or not match_data:
                    continue
                mode = match_data.get('metadata', {}).get('mode', '').lower()
                if mode != "competitive" and mode != "ranked":  # differ by API
                    normal_games += 1

        embed = discord.Embed(title=f"Valorant Info: {name}#{tag}", color=discord.Color.blue())
        embed.add_field(name="Level", value=str(level), inline=True)
        embed.add_field(name="Rank", value=rank, inline=True)
        embed.add_field(name="Ranked Games Played", value=str(ranked_games), inline=True)
        embed.add_field(name="Normal Games (recent 20)", value=str(normal_games), inline=True)

        await interaction.followup.send(embed=embed)


    async def cog_unload(self):
        await self.session.close()

async def setup(bot):
    await bot.add_cog(Valorant(bot))
