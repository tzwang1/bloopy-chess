import React, { Component } from 'react';
import Draggable from 'react-draggable';

class WhiteQueen extends Component {
    constructor(props) {
        super(props)
        this.state = {
            gridPosition: {
                x: 0,
                y: 0
            }
        }
        this.tileSize = props.tileSize;
        this.matrixPos = this.props.pos;
    }
    
    onStart = () => {
        // console.log(this.state.pos);
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: ++activeDrags});
    }

    onStop = (event, drag) => {
        let activeDrags = this.state.activeDrags
        this.setState({activeDrags: --activeDrags});
    }

    adjustPos = (pos) => {
        let new_pos;
        if(Math.abs(pos % this.tileSize) > Math.floor(this.tileSize/2)) {
            if(pos > 0) {
                new_pos = pos + (this.tileSize - (pos % this.tileSize));
            } else {
                new_pos = pos - (this.tileSize + (pos % this.tileSize));
            }
        } else {
            new_pos = pos - (pos % this.tileSize);
        }
        return new_pos
    }

    onControlledDrag = (e, position) => {
        let {x, y} = position;
        // console.log("position", position);
        let oldGridX = this.state.gridPosition.x;
        let oldGridY = this.state.gridPosition.y;

        x = this.adjustPos(x);
        y = this.adjustPos(y);

        this.setState({gridPosition: {x, y}});
    
        let newRow = ((y - oldGridY) / this.tileSize) + this.matrixPos[0];
        let newCol = ((x - oldGridX) / this.tileSize) + this.matrixPos[1];
        this.matrixPos = [newRow, newCol];
    }
    
    onControlledDragStop = (e, position) => {
        this.onControlledDrag(e, position);
        this.onStop();
    }
    
    render() {
        // console.log("Rendering black bishop");
        // console.log("Controlled Position", this.state.gridPosition);
        // console.log("Position", this.matrixPos);
        const gridPosition = this.state.gridPosition;
        const dragHandlers = {onStart: this.onStart, onStop: this.onControlledDragStop};
        return(
            <Draggable disabled={false} position={gridPosition} bounds="parent" {...dragHandlers}>
                 <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 45 45" height="100%">
                    <g
                        fill="#fff"
                        fillRule="evenodd"
                        stroke="#000"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                        strokeLinejoin="round">
                        <path d="M8 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM24.5 7.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM41 12a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM16 8.5a2 2 0 1 1-4 0 2 2 0 1 1 4 0zM33 9a2 2 0 1 1-4 0 2 2 0 1 1 4 0z" />
                        <path
                        d="M9 26c8.5-1.5 21-1.5 27 0l2-12-7 11V11l-5.5 13.5-3-15-3 15-5.5-14V25L7 14l2 12z"
                        strokeLinecap="butt"
                        />
                        <path
                        d="M9 26c0 2 1.5 2 2.5 4 1 1.5 1 1 .5 3.5-1.5 1-1.5 2.5-1.5 2.5-1.5 1.5.5 2.5.5 2.5 6.5 1 16.5 1 23 0 0 0 1.5-1 0-2.5 0 0 .5-1.5-1-2.5-.5-2.5-.5-2 .5-3.5 1-2 2.5-2 2.5-4-8.5-1.5-18.5-1.5-27 0z"
                        strokeLinecap="butt"
                        />
                        <path d="M11.5 30c3.5-1 18.5-1 22 0M12 33.5c6-1 15-1 21 0" fill="none" />
                    </g>
                </svg>
            </Draggable>
        );
    }
}

export default WhiteQueen;