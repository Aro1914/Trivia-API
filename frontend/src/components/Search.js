import React, { Component } from 'react';
import styles from '../stylesheets/FormView.module.css';

class Search extends Component {
  state = {
    query: '',
  };

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query);
  };

  handleInputChange = () => {
    this.setState({
      query: this.search.value,
    });
  };

  render () {
    return (
      <form onSubmit={this.getInfo} className={styles.form}>
        <input
          placeholder='Search questions...'
          ref={(input) => (this.search = input)}
          onChange={this.handleInputChange}
        />
        <input type='submit' value='Submit' className='button' />
      </form>
    );
  }
}

export default Search;
