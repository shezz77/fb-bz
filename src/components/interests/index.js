import React from 'react';

const InterestIndex = props => {
    return (
        <div className="row">

            <div className="col-md-6">
                <div className="form-group">
                    <label>Search Interests:</label><br/>
                    <input type="text" id="interest" className="form-control"
                                                                 name="interest"/>
                </div>
            </div>
        </div>
    );
};

export default InterestIndex;