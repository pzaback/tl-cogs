import discord
import clashroyale
from redbot.core import commands, Config, checks

credits = "By: Kingslayer | LeGeND Gaming"
creditIcon = "https://cdn.discordapp.com/emojis/709796075581735012.gif?v=1"

class LegendEsports(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        self.tags = self.bot.get_cog('ClashRoyaleTools').tags
        self.constants = self.bot.get_cog("ClashRoyaleTools").constants # will I even use it?
        self.config = Config.get_conf(self, identifier=324546534)
        default_global = {'allowed_users': []}
        default_member = {"command_used": False}
        default_guild = {"Challengert": 744084523767300097,
                         "Academyt": 643462706094931989,
                         "Verified": 702491401107144725}
        self.config.register_guild(**default_guild)
        self.config.register_member(**default_member)
        self.config.register_global(**default_global)
        
        

    async def crtoken(self):
        # Clash Royale API
        token = await self.bot.get_shared_api_tokens("clashroyale")
        if token['token'] is None:
            print("CR Token is not SET. Use !set api clashroyale token,YOUR_TOKEN to set it")
        self.cr = clashroyale.official_api.Client(token=token['token'],
                                                  is_async=True,
                                                  url="https://proxy.royaleapi.dev/v1")
    
    @commands.command()
    @commands.guild_only()
    async def tryouts(self, ctx, user: discord.Member = None):
        for_self = False
        if user is None:
            user, for_self = ctx.author, True
        command_used = await self.config.member(user).command_used()
        if command_used is False or await self.bot.is_mod(ctx.author):
            if await self.bot.is_mod(ctx.author) or for_self:
                player_tag = self.tags.getTag(userID = user.id)
                if player_tag is None:
                    return await ctx.send("No tag saved, use the command `!save <your tage here>`")

                else:
                    try:
                        player_data = await self.cr.get_player(player_tag)
                    except clashroyale.RequestError:
                        return await ctx.send("Can't reach the supercell servers at the moment")

                    pb = player_data.bestTrophies
                    max_wins = player_data.challengeMaxWins
                    top_ladder_finisher = False
                    top_global_finish = False
                    ccwins = 0
                    gcwins = 0
                    ign = player_data.name

                    verify_id = await self.config.guild(ctx.guild).Verified()
                    verified_role = await ctx.guild.get_role(verify_id)
                    user.add_roles(verified_role)

                    for badge in player_data.badges: # Credit to Generaleoley 
                        if badge.name == 'Classic12Wins':
                            ccwins = badge.progress
                        elif badge.name == 'Grand12Wins':
                            gcwins = badge.progress
                        elif badge.name == "LadderTournamentTop1000_1":
                            top_global_finish = True
                        elif badge.name == "LadderTop1000_1":
                            top_ladder_finisher = True

                    if (top_ladder_finisher) or ((gcwins >= 1 or ccwins >= 10) and pb >= 6600) or (top_global_finish and max_wins >= 17):
                        maintserver = self.bot.get_guild(740567594381213727)
                        channel = maintserver.get_channel(743498231517806654)
                        invite = await channel.create_invite(max_uses=1)
                        embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                        embed.add_field(name="Team Eligible for:", value="Main Team", inline=True)
                        embed.add_field(name="Personal Best:", value=pb, inline=True)  
                        embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                        embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                        embed.add_field(name="Max Wins", value=max_wins, inline=True)
                        embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                        embed.set_footer(text=credits, icon_url=creditIcon)
                        await ctx.send(embed=embed)
                        await user.send("Hey! {}, You are eligible to tryout for the LeGeND Main Team. Please join the server link given below, **DON'T SHARE IT WITH ANYONE** as its a one time link and will expire after one use.".format(user.mention))
                        await user.send(invite)
                        await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")
                        try:
                            final_name = ign + " | Tryouts"
                            await user.edit(nick=final_name)
                        except discord.HTTPException:
                            return await ctx.send("Not enough permissions")

                        allowed_users = await self.config.allowed_users()
                        allowed_users.append(user.id)
                        await self.config.allowed_users.set(allowed_users)
                        await self.config.member(user).command_used.set(True)

                    elif pb >= 5600 and (ccwins >= 1 or gcwins >= 1):
                        embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                        embed.add_field(name="Team Eligible for:", value="Challenger Team", inline=True)
                        embed.add_field(name="Personal Best:", value=pb, inline=True)  
                        embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                        embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                        embed.add_field(name="Max Wins", value=max_wins, inline=True)
                        embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                        embed.set_footer(text=credits, icon_url=creditIcon)
                        await ctx.send(embed=embed)
                        await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")
                        roleid = await self.config.guild(ctx.guild).Challengert()
                        role = ctx.guild.get_role(roleid)
                        await user.add_roles(role)
                        try:
                            final_name = ign + " | Tryouts"
                            await user.edit(nick=final_name)
                        except discord.HTTPException:
                            return await ctx.send("Not enough permissions")
                        await self.config.member(user).command_used.set(True)
                    else:
                        embed = discord.Embed(colour=0x00FFFF, url="https://royaleapi.com/team/legend-esports", title="LeGeND eSports Tryout")
                        embed.add_field(name="Team Eligible for:", value="Academy Team", inline=True)
                        embed.add_field(name="Personal Best:", value=pb, inline=True)  
                        embed.add_field(name="Grand Challenges Won", value=gcwins, inline=True)
                        embed.add_field(name="Classic Challenges Won", value=ccwins, inline=True)
                        embed.add_field(name="Max Wins", value=max_wins, inline=True)
                        embed.add_field(name="Top Global Tournament Finish", value=top_global_finish, inline=True)
                        embed.set_footer(text=credits, icon_url=creditIcon)
                        await ctx.send(embed=embed)
                        await user.send("Please fill out this google form https://docs.google.com/forms/d/1uptjI7VcBjoev9n45JZTFTqdjWD7PUd4H6uL-zSy-UE/edit")
                        roleid = await self.config.guild(ctx.guild).Academyt()
                        arole = ctx.guild.get_role(roleid)
                        await user.add_roles(arole)
                        try:
                            final_name = ign + " | Tryouts"
                            await user.edit(nick=final_name)
                        except discord.HTTPException:
                            return await ctx.send("Not enough permissions")
                        await self.config.member(user).command_used.set(True)

            else:
                await ctx.send("You are not allowed to use this commmand for other users")

        else:
            await ctx.send("You can't use the command more than once for a user")    

    @commands.command()
    @commands.guild_only()
    async def verify(self, ctx):
        player_tag = self.tags.getTag()
        if player_tag is None:
            return await ctx.send("Player tag not saved, use `!save <#your player tag here>")
        try:
            player_data = self.cr.get_player(player_tag)
            ign = player_data.name
        except clashroyale.RequestError:
            return await ctx.send("Can't reach the supercell servers")
        name = ign + " | Verified"
        verify_id = await self.config.guild(ctx.guild).Verified()
        verified_role = await ctx.guild.get_role(verify_id)
        ctx.author.add_roles(verified_role)
        try:
            ctx.author.edit(name=name)
        except discord.HTTPException:
            return await ctx.send("Not enough permissions to change name.")
        await ctx.send("Roles have been added and nickname has been changed")

    @commands.command()
    @checks.admin_or_permissions()
    @commands.guild_only()
    async def setacademytryoutrole(self, ctx, role: discord.Role):
        await self.config.guild(ctx.guild).Academyt.set(role.id)
        await ctx.send("The academy tryout role is now considered as {}".format(role.id))

    @commands.command()
    @checks.admin_or_permissions()
    @commands.guild_only()
    async def setchallengertryoutrole(self, ctx, role: discord.Role):
        await self.config.guild(ctx.guild).Challengert.set(role.id)
        await ctx.send("The Challenger tryout role is now considered as {}".format(role.id))

    @commands.command()
    @checks.admin_or_permissions()
    @commands.guild_only()
    async def setverifiedrole(self, ctx, role: discord.Role):
        await self.config.guild(ctx.guild).Verified.set(role.id)
        await ctx.send("The Verified role is now considered as {}".format(role.id))

    @commands.command()
    @checks.admin_or_permissions()
    @commands.guild_only()
    async def setacademytryoutrole(self, ctx, role: discord.Role):
        await self.config.guild(ctx.guild).Academyt.set(role.id)
        await ctx.send("The academy tryout role is now considered as {}".format(role.id))

    @commands.command()
    @checks.mod_or_permissions()
    @commands.guild_only()
    async def resettryoutstatus(self, ctx, user: discord.Member):
        await self.config.member(user).command_used.set(False)
        user_lst = await self.config.allowed_users() 
        new_lst = [value for value in user_lst if value != user.id]
        await self.config.allowed_users.set(new_lst)   
        await ctx.send("Users status has been reset")

    @commands.command()
    @commands.guild_only()
    @checks.mod_or_permissions()
    async def forceallow(self, ctx, user:discord.Member):
        async with self.config.allowed_users() as lst:
            lst.append(user.id)
        await self.config.member(user).command_used.set(True)
        await ctx.send("User has been allowed")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        guild = self.bot.get_guild(740567594381213727)
        channel = guild.get_channel(744087559948337172)
        if guild.id == 740567594381213727:
            allowed_users = await self.config.allowed_users()
            if member.id in allowed_users:
                await member.send("Welocome to the Legend Main Team tryout server {}, please go through the rules and ping one of the tryout managers in the respective chat and stay patient, please keep in mind, upon the completion of your tryouts you will be removed from the server.".format(member.mention))
                embed = discord.Embed(colour=0x00FFFF, title="New user joined", description="{} joined and had the requirements to join. Tryouts role added to the user.".format(member.mention))
                await channel.send(embed=embed)
                role = guild.get_role(744088646625263676)
                await member.add_roles(role)
            else:
                embed = discord.Embed(colour=0x00FFFF, title="New user joined", description="{} joined, The user was kicked out because he didn't have the required permissions".format(member.mention))
                await channel.send(embed=embed)
                await member.send("Please join our eSports server first and then you will be allowed to give tryouts as per your stats, you will be kicked from this server for now, join us at https://discord.gg/E34AsPr")
                await member.kick()

    