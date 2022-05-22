import { Component, OnInit } from '@angular/core';
import {MatSnackBar} from "@angular/material/snack-bar";

@Component({
  selector: 'app-inference-form',
  templateUrl: './inference-form.component.html',
  styleUrls: ['./inference-form.component.scss']
})
export class InferenceFormComponent implements OnInit {

  tags: string[] = []
  newTag: string = ''

  constructor(private _snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  query(): void {
    this.tags = ["aaa"];
  }

  submitFeedback() {
    this.tags = [];
    this.newTag = '';
    this._snackBar.open('Thank you!', 'Close', {duration: 3000});
  }

}
