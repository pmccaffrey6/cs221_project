from flask import Flask, render_template, request, url_for, flash, redirect

import pandas as pd
import numpy as np
import deepchem as dc
from scipy.spatial.distance import cosine

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cs221'

sim_mat = pd.read_csv('sim_m2v_table.csv')
chemical_index = sim_mat.index.values
smiles_mol2vec = pd.read_csv('smiles_and_mol2vec.tsv', sep='\t', dtype={
    'pfam_id':str,
    'CanonicalSMILES':str,
    'mol2Vec':object
})
pfam_name_lookup = pd.read_csv('pfam_name_lookup.tsv', sep='\t')

K = 5

messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@app.route('/create/', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        K = int(request.form['neighbors'])

        if not title:
            flash('Job Title is required!')
        elif not content:
            flash('Chemical Structure is required!')

        else:
            ###
            # perform search on chemicals
            ###
            featurizer = dc.feat.Mol2VecFingerprint()
            smiles_mol2vec['mol2Vec'] = [featurizer.featurize(i) for i in smiles_mol2vec['CanonicalSMILES']]
            m2v_query = featurizer.featurize(content)
            print(f"featurized query {content}: {m2v_query}")
            print(f"dtypes {smiles_mol2vec.dtypes}; {smiles_mol2vec['mol2Vec'].values[0]}")

            query_sim = np.array( [cosine(m2v_query.reshape(300,-1), i) for i in smiles_mol2vec['mol2Vec'].values ])
            #closest_match_idx = np.argmin(query_sim)
            closest_match_idx = np.argpartition(query_sim, -K)[-K:]
            #closest_match_smiles = chemical_index[closest_match_idx]
            closest_match_smiles = [chemical_index[i] for i in closest_match_idx]
            #closest_match_pfam = smiles_mol2vec['pfam_id'].values[closest_match_idx]
            closest_match_pfam = [smiles_mol2vec['pfam_id'].values[i] for i in closest_match_idx]

            pfam_match_statements = [f"{i}; ({pfam_name_lookup[pfam_name_lookup['PFAM_ACCESSION']==i]['PFAM_NAME'].values[0]})" for i in closest_match_pfam]

            messages.append({
                'Job Title': title,
                'Chemical Structure': content,
                'PFAM Matches': ',     '.join(pfam_match_statements),
            })
            return redirect(url_for('index'))

    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)
