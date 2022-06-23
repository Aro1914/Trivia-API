import React, { Component } from 'react';
import '../stylesheets/Question.css';
import $ from 'jquery';

const base_url = '/api/v0.1.0';

class Question extends Component {
  constructor() {
    super();
    this.state = {
      visibleAnswer: false,
      originalCategories: [
        'Science',
        'Art',
        'Geography',
        'History',
        'Entertainment',
        'Sports'
      ],
      id: 0,
      rating: 0
    };
  }

  componentDidMount () {
    const { id, rating } = this.props;
    this.setState({
      id: id,
      rating: rating
    });
  }

  createRating () {
    const ratings = [];
    for (let index = 1; index <= 5; index++) {
      ratings.push(
        <span className='rate' key={index} onClick={() => this.updateRating(index)}>{this.state.rating >= (index) ? '💛' : '🖤'}</span>
      );
    }
    return ratings;
  }

  updateRating (rating) {
    $.ajax({
      url: `${base_url}/questions/${this.state.id}`,
      type: 'PATCH',
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({ rating: rating }),
      xhrFields: {
        withCredentials: true,
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          rating: rating
        });
        return;
      },
      error: (error) => {
        alert('Unable to update rating: ' + error.message);
        return;
      },
    });
  }

  flipVisibility () {
    this.setState({ visibleAnswer: !this.state.visibleAnswer });
  }

  render () {
    const { question, answer, category, difficulty } = this.props;
    return (
      <div className='Question-holder'>
        <div className='Question'>{question}</div>
        <div className='Question-status'>
          <img
            className='category'
            alt={`${category.toLowerCase()}`}
            src={`${this.state.originalCategories.some(el => el === category) ? category.toLowerCase() : 'new'}.svg`}
          />
          <div className='difficulty'>Difficulty: {difficulty}</div>
          <img
            src='delete.png'
            alt='delete'
            className='delete'
            onClick={() => this.props.questionAction('DELETE')}
          />
        </div>
        <div
          className='show-answer button'
          onClick={() => this.flipVisibility()}
        >
          {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
        </div>
        <div className='answer-holder'>
          <span
            style={{
              visibility: this.state.visibleAnswer ? 'visible' : 'hidden',
            }}
          >
            Answer: {answer}
          </span>
        </div>
        <div className='rating'>
         Rating: {this.createRating()}
        </div>
      </div>
    );
  }
}

export default Question;
