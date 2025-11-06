class costFunction:
    def cost_function(anwser_vector, correct_vector): #anwser_vector (forward pass): last layer of results (0-9) where for example [0.1, 0.45, ...], uncorrected result of nn, correct_vector: ideal anwser (pure 1)
        if(len(anwser_vector) == len(correct_vector)):
            result = 0
            for i in range (len(anwser_vector)):
                difference = correct_vector[i] - anwser_vector[i]
                result += difference * difference
            return result
        return ValueError