"""
Control GMP with a game controler.

This script can be modified to send system events or AppleScripts which you could use to get greater control over your computer.

We use requests to get the URLs which can be used to control GMP.

Buttons are logged for convenience (and debugging).
"""
import pygame, logging, sys, requests

logging.basicConfig(stream = sys.stdout, level = 'INFO') # Set up the root logger.

pygame.init() # Initialise Pygame.

if __name__ == '__main__': # Only run if this script is called directly.
 buttons = { # Could change the values to be lambdas or whatever you wanted.
  0: 'previous',
  2: 'next',
  3: 'volume_up',
  1: 'volume_down',
  8: 'play',
  9: 'stop'
 }
 if not pygame.joystick.get_count(): # There are no joysticks detected.
  logging.critical('Please connect a joystick.') # Complain, noisily!
 else: # We have joystick(s).
  logging.info('Joysticks detected: %s.', pygame.joystick.get_count()) # Say how many in case there are multiples.
  j = pygame.joystick.Joystick(0) # Create a Joystick from the first available device.
  j.init() # Initialise.
  logging.info('Using joystick: %s.', j.get_name()) # Let the user know which one was selected.
  while 1: # Main event loop.
   for e in pygame.event.get(): # Get all the events.
    if e.type == pygame.JOYBUTTONDOWN: # A joystick button was pressed.
     if e.button in buttons: # This button has an associated value in the buttons dict.
      try: # Don't let it trace, since that causes Pygame to exit.
       response = requests.get('http://127.0.0.1:4673/%s' % buttons[e.button], auth = ('gmp', 'LetMeIn')) # Get the URL specified in the value.
       logging.info('Button %s (%s) => %s.', e.button, buttons[e.button], response.status_code)
      except Exception as err:
       logging.warning('Button %s (%s) threw the following traceback:', e.button, buttons[e.button])
       logging.exception(err)
     else:
      logging.info('Button: %s.', e.button)
    elif e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.unicode == 'q'): # Allow the program to be quit gracefully.
     pygame.quit()
     sys.exit()
