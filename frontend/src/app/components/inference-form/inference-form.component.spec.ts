import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InferenceFormComponent } from './inference-form.component';

describe('InferenceFormComponent', () => {
  let component: InferenceFormComponent;
  let fixture: ComponentFixture<InferenceFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InferenceFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InferenceFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
