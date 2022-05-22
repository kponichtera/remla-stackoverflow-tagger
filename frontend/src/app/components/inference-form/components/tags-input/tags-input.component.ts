import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {MatChipInputEvent} from "@angular/material/chips";
import {FormControl} from "@angular/forms";
import {COMMA, ENTER} from "@angular/cdk/keycodes";

@Component({
  selector: 'app-tags-input',
  templateUrl: './tags-input.component.html',
  styleUrls: ['./tags-input.component.scss']
})
export class TagsInputComponent implements OnInit {

  separatorKeysCodes: number[] = [ENTER, COMMA];

  private _newTag: string = ''

  @Input()
  disabled: boolean = false;

  @Input()
  tags: string[] = []

  @Output()
  tagsChange = new EventEmitter<string[]>();

  @Output()
  newTagChange = new EventEmitter<string>();

  constructor() { }

  ngOnInit(): void {
  }

  add(): void {
    const value = this._newTag.trim();

    if (value) {
      this.tags.push(value);
      this.tagsChange.emit(this.tags);
    }

    // Clear the input value
    this._newTag = ''
  }

  remove(tag: string): void {
    const index = this.tags.indexOf(tag);
    if (index >= 0) {
      this.tags.splice(index, 1);
      this.tagsChange.emit(this.tags)
    }
  }

  @Input()
  get newTag(): string {
    return this._newTag;
  }

  set newTag(value: string) {
    this._newTag = value;
    this.newTagChange.emit(value);
  }

}
