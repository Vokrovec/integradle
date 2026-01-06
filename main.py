import os
import discord
from discord.ext import commands
from discord import ui
import dotenv
from generator import save_as_latex_image_io, generate_integral
import random

# --- Bot Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- The Modal (Pop-up Window) ---
class AnswerModal(ui.Modal, title='Submit your Answer'):
    # The text input field
    user_input = ui.TextInput(label='Result', placeholder='e.g., 0.512, 0.324, 4.274')

    def __init__(self, correct_answer_obj):
        super().__init__()
        self.correct_answer = correct_answer_obj

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Evaluate both to decimals for a fair comparison
            if abs(self.correct_answer.evalf() - float(self.user_input.value)) < 10**-3:
                await interaction.response.send_message(f"✅ Correct! The answer is {self.user_input.value}.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Not quite. Try again!", ephemeral=True)
        except Exception as e:
            print(e)
            await interaction.response.send_message("⚠️ Error: Please enter a valid number or fraction.", ephemeral=True)

class SolutionView(ui.View):
    def __init__(self, answer):
        super().__init__(timeout=None) # Button stays active
        self.answer = answer
    @ui.button(label="Check Answer", style=discord.ButtonStyle.green)
    async def check_answer(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.send_modal(AnswerModal(self.answer))

    @ui.button(label="View Answer", style=discord.ButtonStyle.red)
    async def view_answer(self, interaction: discord.Interaction, button: ui.Button):
        image = save_as_latex_image_io(self.answer)
        file = discord.File(fp=image, filename="solution.png")
        await interaction.response.send_message(
            "The answer is:", 
            file=file,
            ephemeral=True)

@bot.command()
async def integral(ctx):
    """Command: !integral"""
    await ctx.send("Generating a fresh integral for you...")
    
    # Generate the image in memory
    seed = random.randint(1, 100000000)
    print(seed)
    problem, answer = generate_integral(seed=seed)
    image = save_as_latex_image_io(problem)
    view = SolutionView(answer)
    # Send to Discord
    file = discord.File(fp=image, filename="problem.png")
    await ctx.send("Can you solve this?", file=file, view=view)

if __name__ == "__main__":
    dotenv.load_dotenv()
    token = str(os.getenv("TOKEN"))
    bot.run(token)
