from abc import ABC, abstractmethod
from google import genai
from google.genai import errors,types
import json
import socket
import os
import re
from datetime import datetime
import random
import logging

logger = logging.getLogger(__name__)

# 1. Define the Interface
class TicTacToeSolver(ABC):
    @abstractmethod
    def get_move(self, game_data: dict) -> int:
        pass

#if os.path.exists("my_api_key.txt"):
with open("my_api_key.txt",'r') as f:
    api_key = f.readline() #os.getenv("GOOGLE_API_KEY")

# 2. Implementation for Gemini Cloud
class GeminiCloudSolver(TicTacToeSolver):
    def __init__(self, api_key):
        self.client = genai.Client(api_key=api_key)
        #self.system_prompt = "Output ONLY a single digit (1-9) for the next move."
     #   self.system_rules = (
     #         "You are a Tic-Tac-Toe strategist"
     #         "Input will be a JSON containing 'game_state', 'empty_slots'",
     #         "Analyze the board for winning lines and opponent threats",
     #         "Keep reasoning only 1 line and provide it in 'reasoning' field",
     #         "and the best available move integer in the 'move' field.",
     #         "read 'empty_slots' again before making the 'move' the move *must be* from emtpy slots"

     #    )
        self.system_rules = (
            "1. Priority: WIN immediately if possible. "
            "2. Secondary: BLOCK opponent if they have 2-in-a-row. "
            "3. Strategy: Prefer the center (5), then corners. "
            "4. Constraint: The 'move' MUST be an integer from 'empty_slots'."
        )

    def visualize_board(self,game_board):
        
        check = lambda x: x if x is not None else " " 
        rows = []

        for i in ['1','4','7']:
            r = f" {check(game_board[i])} | {check(game_board[str(int(i) + 1)])} | {check(game_board[str(int(i)+2)])}"
            rows.append(r)
        return "\n-----------\n".join(rows)


    def get_move(self, game_data: dict) -> int:
        empty_slots = game_data.get('empty_slots', [])
        model = "gemini-3-flash-preview" #"gemini-3.1-flash-lite-preview" #"gemini-1.5-flash"
        # Use your new visualize_board method to help the AI "see"
        board_str = self.visualize_board(game_data['game_state'])
        logger.info(f"board {board_str}")

        user_input = (
            f"Visual Board:\n{board_str}\n"
            f"Available Slots: {empty_slots}\n"
            "Think step-by-step and pick your move."
        )

        logger.info(f"sending {user_input} to bot")

        response = self.client.models.generate_content(
            model =  model, #"gemini-2.5-flash-lite",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction = self.system_rules,
                #max_output_tokens=500,
                #temperature=0.1,
                response_mime_type = "application/json",
                response_schema = {
                    "type" : "OBJECT",
                    "properties" : {
                        "move" : {"type" : "INTEGER"},
                    },
                    "required" : ["move"]
                }
            )
        )
        try:
            if not response or not response.candidates:
                logger.error("empty candidate list")
                raw_response = {}
            else:
                logger.debug(f"finish reason: {response.candidates[0].finish_reason}")
                raw_response = response.text
            text = json.loads(raw_response)
            logger.info(f"got response from bot {text}")
            move = str(text.get('move'))
        except Exception as e:
            logger.error(f"error from json {e} {raw_response} ")
            move = None
        
        if not move or not move in empty_slots:
            logger.error(f"bot provided wrong move {move}, reverting bot choice")
            move = empty_slots[0]

        return move


# 3. Future Placeholder for Local Fallback
class LocalGemmaSolver(TicTacToeSolver):
    def get_move(self, game_data: dict) -> int:
        # Later, you will put your Ollama/llama.cpp logic here
        logger.info("Running locally on M1...")
        return random.choice(game_data['empty_slots'])

cloud_solver = GeminiCloudSolver(api_key)
local_solver = LocalGemmaSolver()

def get_move_from_bot(game_state):
    try:
        ##solver = GeminiCloudSolver(api_key)
        return cloud_solver.get_move(game_state)
    except (socket.gaierror, errors.APIError,ConnectionError,errors.ClientError) as e:
        ##solver = LocalGemmaSolver()
        logger.error("API error {e}")
        return local_solver.get_move(game_state)
    #except Exception as e:
        ## will add a logger here later, don't want system to crash
        #return random.choice(game_state['empty_slots'])

if __name__ == "__main__":

    def visualize_board(game_board):
        
        check = lambda x: x if x is not None else " " 
        rows = []

        for i in ['1','4','7']:
            r = f" {check(game_board[i])} | {check(game_board[str(int(i) + 1)])} | {check(game_board[str(int(i)+2)])}"
            rows.append(r)
        return "\n-----------\n".join(rows)

    game_state = {'game_state' :{'1': None, '2': None, '3': None,
                      '4': None, '5': 'o', '6': 'o',
                      '7': None, '8': 'x', '9': None},'empty_slots' : [1,2,3,4,7,9]}
    place = get_move_from_bot(game_state)
    ##print(visualize_board(game_state['game_state']))
    print(place)
