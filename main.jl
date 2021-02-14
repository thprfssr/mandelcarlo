using Distributed
using Printf

@everywhere using Distributions
@everywhere include("mandelbrot.jl")

function integrate(threshold, x_range, y_range, samples)
	x_min, x_max = x_range
	y_min, y_max = y_range

	N_I = 0
	N_T = samples
	N_I = @distributed (+) for _ = 1:samples
		x = rand(Uniform(x_min, x_max))
		y = rand(Uniform(y_min, y_max))
		c = x + y * im

		Int(is_mandelbrot(c, threshold))
	end

	q = N_I / N_T
	u_q = sqrt(q * (1 - q)) / sqrt(samples)
	A_T = (x_max - x_min) * (y_max - y_min)
	A_I = q * A_T
	u_A_I = u_q * A_T

	return A_I, u_A_I
end



#define X_MIN (-2)
#define X_MAX (0.58)
#define Y_MIN (0)
#define Y_MAX (1.20)



x_range = (-2, 0.5)
y_range = (0, 1.2)
samples = 10000000
for threshold = 1000:500:10000
	A, u_A = integrate(threshold, x_range, y_range, samples)
	A *= 2
	u_A *= 2
	@printf("%d\t%f\t%f\n", threshold, A, u_A)
end
