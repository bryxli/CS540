from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt

def load_and_center_dataset(filename):
    file = np.load(filename)
    dataset = file - np.mean(file,axis=0)
    return dataset

def get_covariance(dataset):
    S = (1/2413) * np.dot(np.transpose(dataset),dataset)
    return S

def get_eig(S, m):
    w,v = eigh(S)
    Lambda = w[-m:]
    U = v[:,-m:]
    idx = Lambda.argsort()[::-1]
    Lambda = Lambda[idx]
    U = U[:,idx]
    return np.diag(Lambda),U

def get_eig_prop(S, prop):
    w,v = eigh(S)
    sum = w.sum()
    count = 0
    for eigenvalue in w:
        if eigenvalue / sum > prop:
            count += 1
    return get_eig(S,count)
    

def project_image(image, U):
    Ucol = U.shape[1]
    projection = 0
    for column in range(Ucol):
        projection += np.dot(np.dot(np.transpose(U[:,column]),image),U[:,column])
    return projection

def display_image(orig, proj):
    orig = np.transpose(orig.reshape(32,32))
    proj = np.transpose(proj.reshape(32,32))
    fig,ax = plt.subplots(nrows = 1,ncols = 2)
    ax[0].set_title("Original")
    ax[1].set_title("Projection")
    orig_bar = ax[0].imshow(orig,aspect='equal')
    proj_bar = ax[1].imshow(proj,aspect='equal')
    fig.colorbar(orig_bar)
    fig.colorbar(proj_bar)
    plt.show()

x = load_and_center_dataset('YaleB_32x32.npy')
S = get_covariance(x)
Lambda, U = get_eig(S, 2)
projection = project_image(x[0], U)
display_image(x[0], projection)