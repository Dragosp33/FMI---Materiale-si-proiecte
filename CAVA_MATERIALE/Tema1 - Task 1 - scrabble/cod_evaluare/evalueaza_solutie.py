def compare_annotations(filename_predicted,filename_gt,verbose=0):
	p = open(filename_predicted,"rt")  	
	gt = open(filename_gt,"rt")  	
	all_lines_p = p.readlines()
	all_lines_gt = gt.readlines()

	#positions and letters	
	number_lines_p = len(all_lines_p)
	number_lines_gt = len(all_lines_gt)

	match_positions = 1
	match_letters = 1
	match_score = 1

	for i in range(number_lines_gt-1):		
		current_pos_gt, current_letter_gt = all_lines_gt[i].split()
		
		if verbose:
			print(i)
			print(current_pos_gt,current_letter_gt)

		try:
			current_pos_p, current_letter_p = all_lines_p[i].split()
			
			if verbose:
				print(current_pos_p,current_letter_p)

			if(current_pos_p != current_pos_gt):
				match_positions = 0
			if(current_letter_p != current_letter_gt):
				match_letters = 0	
		except:
			match_positions = 0
			match_letters = 0		
	try:
		#verify if there are more possitions + letters lines in the prediction file
		current_pos_p, current_letter_p = all_lines_p[i+1].split()
		match_positions = 0
		match_letters = 0

		if verbose:
			print("EXTRA LINE:")
			print(current_pos_p,current_letter_p)
			
	except:
		pass



	points_positions = 0.05 * match_positions
	points_letters = 0.02 * match_letters	

	#scores
	last_line_p = all_lines_p[-1]
	score_p = last_line_p.split()
	last_line_gt= all_lines_gt[-1]
	score_gt = last_line_gt.split()
	
	if verbose:
		print(score_p,score_gt)

	if(score_p != score_gt):
		match_score = 0

	points_score = 0.02 * match_score

	return points_positions, points_letters,points_score

#change this on your machine pointing to your results (txt files)
predictions_path_root = "/Users/bogdan/Dropbox/CAVA-scrabble/CAVA-2022-TEMA1/evaluare/fisiere_solutie/331_Alexe_Bogdan/"

#change this on your machine to point to the ground-truth test
gt_path_root = "/Users/bogdan/Dropbox/CAVA-scrabble/CAVA-2022-TEMA1/antrenare/"


#change this to 1 if you want to print results at each turn
verbose = 1
total_points = 0
for game in range(1,6):
	for turn in range(1,21):
		
		name_turn = str(turn)
		if(turn< 10):
			name_turn = '0'+str(turn)

		filename_predicted = predictions_path_root + str(game) + '_' + name_turn + '.txt'
		filename_gt = gt_path_root + str(game) + '_' + name_turn + '.txt'

		game_turn = str(game) + '_' + name_turn
		points_position = 0
		points_letters = 0
		points_score = 0		

		try:
			points_position, points_letters, points_score = compare_annotations(filename_predicted,filename_gt,verbose)
		except:
			print("For image: ", game_turn, " encountered an error")

		print("Image: ", game_turn, "Points position: ", points_position, "Points letters: ",points_letters, "Points score: ", points_score)
		total_points = total_points + points_position + points_letters + points_score

print(total_points)